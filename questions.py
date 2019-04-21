from fuzzywuzzy import fuzz
from fuzzywuzzy import process

questions_global = [["все возможные ходы", "какие ходы существуют"]
,["как лучше сходить", "какой лучший ход", "подскажи лучший ход", "как походить в данной ситуации", "как мне ходить" , "как я могу походить", "как я могу сходить", "покажи лучший ход", "подскажи какой лучший ход в данной ситуации"],
["как ходит пешка", "покажи возможные ходы у пешки"],
["как ходит король", "покажи возможные ходы у короля"],
["как ходит ферзь", "покажи возможные ходы у ферзя", "как ходит королева", "покажи возможные ходы у королевы"],
["как ходит ладья", "покажи возможные ходы у ладьи"],
["как ходит конь", "покажи возможные ходы у коня"],
["как ходит офицер", "как ходит слон", "какие возможные ходы у офицера", "какие возможные ходы у слона"],
["возможна ли рокировка", "можно ли сделать рокировку"],
["оцени ситуацию на столе"]]

def find_max_ratio(questions, question):
    max = -1
    ans = ""
    for t in questions:
        ratio = fuzz.token_sort_ratio(t, question)
        # print(t, ratio)
        if max < ratio:
            max = ratio
            ans = t
    return [questions.index(ans), max]

def find_best_match(question):
    ans = [0, -1]
    indx = 0
    for i in range(len(questions_global)):   
        ret = find_max_ratio(questions_global[i], question)
        if ret[1] > ans[1]:
            ans = ret
            indx = i
    if ans[1] < 50:
        return[-1, -1]
    return [indx, ans[1]]

#ans = find_best_match(questions, "рокировка")
#print(questions[ans[0]][ans[1]], ans[2])