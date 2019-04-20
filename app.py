from flask import Flask, render_template, request, redirect, request, Response
import jinja2
import os
import json 
from movesfinder import MovesFinder, CheckFunc
import questions
import answers

app = Flask(__name__)


#Read JSON data into the datastore variable
json_var = json.load(open("mock.json", 'r'))

#Use the new datastore datastructure

keys = json_var.keys()
keys_arr = []
for key in keys:
	keys_arr.append(key)
pos = -1

best_move_fen = ""
repeat_flag = 0
help_asked = 0


@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/change')
def chance():
	return redirect('/')

@app.route('/post', methods=['GET','POST'])
def post():
	if request.method == 'POST':
		return render_template('post.html')
	return render_template('get.html')

@app.route('/get_help_start', methods=['POST'])
def get_help_start():
	global help_asked
	help_asked = help_asked - 1
	json_req = request.get_json()
	movesfinder = MovesFinder()
	checkFunc = CheckFunc()

	game_status = movesfinder.how_best_move(json_req["board"])
	game_state = checkFunc.check_state(json_req["board"])
	answer = ""
	
	if game_state == 1:
		answer = answers.get_warning_check()
	elif game_status[2] == 2:
		answer = answers.get_setup_mate()
	
	return json.dumps({"answer": answer})

@app.route('/get_help_end', methods=['POST'])
def get_help_end():
	global best_move_fen
	global repeat_flag
	json_req = request.get_json()
	movesfinder = MovesFinder()
	checkFunc = CheckFunc()
	answer = ""

	game_state = checkFunc.check_state(json_req["board"])

	print(json_req["board"])
	print(best_move_fen)
	print("repeat flag = ", repeat_flag)
	if game_state == 2:
		answer = answers.get_victory()
	elif json_req["board"] == best_move_fen and repeat_flag < 1:
		answer = answers.get_good_boy()
		repeat_flag = 5
	repeat_flag = repeat_flag - 1
	print("repeat flag = ", repeat_flag)
	print("answer = ", answer)

	return json.dumps({"answer": answer})


@app.route('/get_help', methods=['POST'])
def get_help():
	global best_move_fen
	global help_asked

	json_req = request.get_json()
	movesfinder = MovesFinder()
	checkFunc = CheckFunc()
	match = questions.find_best_match(json_req["question"])
	
	possible_moves = []
	answer = "haha"

	if match[0] == -1:
		answer = answers.get_bad_question()
		ret = {}
		ret["answer"] = answer
		return json.dumps({"answer": answer})

	game_status = movesfinder.how_best_move(json_req["board"])
	best_move_fen = checkFunc.upd_fen(json_req["board"], game_status[3])
	print ("best_fen = ",best_move_fen)
	if match[0] == 0:
		answer = answers.get_answer_all_moves()
		possible_moves = movesfinder.get_list_moves(json_req["board"])
	elif match[0] == 1:		
		if help_asked > 0:
			answer = answers.get_help_cooldown()
		else:
			help_asked = 2
			figure_name = answers.get_figure(game_status[1])
			figure_name_rod = answers.get_figure_1(game_status[1])
			move_status = game_status[2]
			print("fig = ", game_status[1])
			print("figure = ",figure_name)
			print("figure rod= ",figure_name_rod)
			print("move status = ", move_status)
			print("uci = ", game_status[3])
			if move_status == 5:
				answer = answers.get_right_castling()
			elif move_status == 6:
				answer = answers.get_left_castling()
			else:
				if move_status == 1:
					answer = answers.get_suggest_kills()
				elif move_status == 0:
					answer = answers.get_suggest_moves()
				elif move_status == 2:
					answer = answers.get_suggest_mate()	
				else:
					answer = answers.get_suggest_check()			
				answer += figure_name_rod + " " + game_status[3][0:2] + " " + game_status[3][2:4]
			possible_moves = game_status[0]
	elif match[0] == 2:
		answer = answers.get_answer_for_pawn_moves()
	elif match[0] == 3:
		answer = answers.get_answer_for_king_moves()
	elif match[0] == 4:
		answer = answers.get_answer_for_queen_moves()
	elif match[0] == 5:
		answer = answers.get_answer_for_rook_moves()
	elif match[0] == 6:
		answer = answers.get_answer_for_knight_moves()
	elif match[0] == 7:
		answer = answers.get_answer_for_bishop_moves()
	elif match[0] == 8:
		situation = checkFunc.check_castling(json_req["board"])
		if len(situation) > 1:
			answer = answers.get_both_castlings()
		elif len(situation) == 0:
			answer = answers.get_castling_is_not_allowed()
		else:
			if situation[0][1][0] == 0:
				answer = answers.get_left_castling()
			else:
				answer = answers.get_right_castling()
	elif match[0] == 10:
		situation = checkFunc.get_crit(json_req["board"])
		diff = situation[0] - situation[1]
		if diff > 15:
			answer = answers.get_answer_for_winning_h()
		elif diff > 4:
			answer = answers.get_answer_for_winning()
		elif diff < -15:
			answer = answers.get_answer_for_losing_h()
		elif diff < -4:
			answer = answers.get_answer_for_losing()
		else:
			answer = answers.get_answer_for_even()
	return json.dumps({"answer": answer, "possible_moves" : possible_moves})

@app.route('/init', methods=['GET'])
def init():
	global pos
	pos = -1
	return ""

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)