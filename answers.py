import random

pawn_moves = "Вот все возможные ходы для ваших пешек"
king_moves = "Вот все возможные ходы короля"
queen_moves = "Вот все возможные ходы ферзя"
bishop_moves = "Вот все возможные ходы для ваших слонов"
knight_moves = "Вот все возможные ходы коней"
rook_moves = "Вот все возможные ходы ладей"
all_moves = "Вот все ходы которые я смогла найти"
suggest_castling = "Пожалуй стоит сделать рокировку"
castling_is_allowed = "Рокируйтесь, конечно"
castling_is_not_allowed = "Не думаю что это по правилам"
winning = "У вас перевес по фигурам"
losing = "Перевес по фигурам у оппонента"
winning_heavily = "У вас сильный перевес по фигурам"
losing_heavily = "Я очень удивлюсь если вы сможете победить"
even_game = "Преимущества по фигурам ни у кого нет"
both_castlings = "Можно сделать обе рокировки"
left_castling = "Можно сделать левую рокировку"
right_castling = "Можно сделать правую рокировку"
suggest_moves = ["Предлагаю походить ", "Думаю стоит сходить "]
suggest_kills = ["Ну это же очевидно! Рубите ", "Рубите ", "Предлагаю съесть "]
suggest_mate = ["Можете поставить мат ", "Ставте мат "]
suggest_check = ["Предлгаю поставить шах ", "Ставте шах "]
suggest_kill_and_check = "Рубите"

warning_check = "Кажется вам поставили шах"
warning_mate = "Кажется вам поставили мат"
setup_mate = "Если сходишь правильно, можешь поставить мат"
good_boy = "А ты послушный"
victory = "Шах и мат! Ты победил! Поздравляю!"
help_cooldown = "Ты только что спрашивал, в этот раз подумай сам. Ты же хочешь научиться играть"
bad_question = ["Я не знаю ответа на этот вопрос", "Подумайте сами", "Я шахматный помощник, а не Алиса"]

def get_answer_all_moves():
    global all_moves
    return all_moves

def get_answer_for_king_moves():
    global king_moves
    return king_moves

def get_answer_for_pawn_moves():
    global pawn_moves
    return pawn_moves

def get_answer_for_queen_moves():
    global queen_moves
    return queen_moves

def get_answer_for_bishop_moves():
    global bishop_moves
    return bishop_moves

def get_answer_for_rook_moves():
    global rook_moves
    return rook_moves

def get_answer_for_knight_moves():
    global knight_moves
    return knight_moves

def get_answer_for_winning():
    global winning
    return winning
def get_answer_for_losing():
    global losing
    return losing
def get_answer_for_winning_h():
    global winning_heavily
    return winning_heavily
def get_answer_for_losing_h():
    global losing_heavily
    return losing_heavily
def get_answer_for_even():
    global even_game
    return even_game
def get_both_castlings():
    global both_castlings
    return both_castlings

def get_left_castling():
    global left_castling
    return left_castling

def get_right_castling():
    global right_castling
    return right_castling

def get_castling_is_not_allowed():
    global castling_is_not_allowed
    return castling_is_not_allowed

def get_suggest_castling():
    global suggest_castling
    return suggest_castling

def get_suggest_moves():
    global suggest_moves
    rand = random.randint(0, len(suggest_moves) - 1)
    return suggest_moves[rand]

def get_suggest_kills():
    global suggest_kills
    return suggest_kills[random.randint(0, len(suggest_kills) - 1)]

def get_suggest_check():
    global suggest_check
    return suggest_check[random.randint(0, len(suggest_check) - 1)]

def get_suggest_mate():
    global suggest_mate
    return suggest_mate[random.randint(0, len(suggest_mate) - 1)]

def get_warning_check():
    global warning_check
    return warning_check

def get_warning_mate():
    global warning_mate
    return warning_mate

def get_setup_mate():
    global setup_mate
    return setup_mate

def get_good_boy():
    global good_boy
    return good_boy

def get_victory():
    global victory
    return victory

def get_help_cooldown():
    global help_cooldown
    return help_cooldown

def get_bad_question():
    global bad_question
    return bad_question[random.randint(0, len(bad_question) - 1)]

def get_answer_from_move(move):
    if "#" in move:
        return "MATE!"
    return "pf"

def get_action(number):
    if number == 0:
        return "ходит"
    if number == 1:
        return "рубит"
    if number == 2:
        return "мат"

def get_figure(ch):
    if ch == "P":
        return "пешка"
    if ch == "Q":
        return "королева"
    if ch == "k":
        return "король"
    if ch == "N":
        return "конь"
    if ch == "B":
        return "слон"
    if ch == "R":
        return "ладья"

def get_figure_1(ch):
    if ch == "P":
        return "пешкой"
    if ch == "Q":
        return "королевой"
    if ch == "k":
        return "королём"
    if ch == "N":
        return "конём"
    if ch == "B":
        return "слоном"
    if ch == "R":
        return "ладьёй"