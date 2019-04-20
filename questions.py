from fuzzywuzzy import fuzz
from fuzzywuzzy import process

questions_global = [["все возможные ходы", "как я могу походить", "как я могу сходить"]
,["как лучше сходить", "какой лучший ход", "подскажи лучший ход", "как походить в данной ситуации"],
["как ходит пешка"],
["как ходит король"],
["как ходит королева"],
["как ходит ладья"],
["как ходит конь"],
["как ходит офицер", "как ходит слон"],
["возможна ли рокировка", "можно ли сделать рокировку"],
["стоит ли сходить"],
["оцени ситуацию на столе"]]

def find_max_ratio(questions, question):
    max = -1
    ans = ""
    for t in questions:
        ratio = fuzz.token_sort_ratio(t, question)
        print(t, ratio)
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