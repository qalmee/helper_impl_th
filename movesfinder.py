import pdb
import chess
import chess.uci
import chess.engine
import config_stock

class MovesFinder:
    _scrf = 5.0
    _ustate = 0
    _estate = 1
    _mstate = 2
    _astate = 3
    _eastate = 4
    _shstate = 5
    _lnstate = 6
    _depth = 10

    def __init__(self):
        path = config_stock.get_stockfish_path()
        self._engine = chess.uci.popen_engine(path)
        self._engine.uci()
        self._info_handler=chess.uci.InfoHandler()
        self._engine.info_handlers.append(self._info_handler)

    def convert_move(self, inp):
        k0 = ord(inp['move'][0]) - ord('a')
        k1 = 7 - ord(inp['move'][1]) + ord('1')
        k2 = ord(inp['move'][2]) - ord('a')
        k3 = 7 - ord(inp['move'][3]) + ord('1')
        return [[k1, k0], [k3, k2]]

    def convert_move_arr(self, inp):
        k0 = ord(inp[0]) - ord('a')
        k1 = 7 - ord(inp[1]) + ord('1')
        k2 = ord(inp[2]) - ord('a')
        k3 = 7 - ord(inp[3]) + ord('1')
        return [[k1, k0], [k3, k2]]


    def find_figure_moves(self, sboard, figure):
        get_indexes = lambda needle, haystack: [i for (y, i) in zip(haystack, range(len(haystack))) if needle == y]
        arr = self.find_figure(sboard, figure)
        figure_moves = self.get_list_moves_uci(sboard)
        figure_positions = []
        for move in figure_moves:
            figure_positions.append(move[0:2])
        good_moves = []
        # print("arr = ",arr)
        # print("figure_moves = ", figure_moves)
        # print("figure_positions = ", figure_positions)
        
        for pos in arr:
            indexes = get_indexes(pos, figure_positions)
            # print("indexes = ", indexes)
            # print("pos = ", pos)
            for indx in indexes:
                print("uci = ", figure_moves[indx], " == ", self.convert_move_arr(figure_moves[indx]))
                good_moves.append(self.convert_move_arr(figure_moves[indx]))
            # print("pos = ", pos)
        # print("good ones = ", good_moves)
        return good_moves

    def find_figure(self, sboard, figure):
        arr = sboard.split('/')
        ret = []
        for i in range(0, 8):
            for j in range(0, min(len(arr[i]), 8)):
                if arr[i][j] == figure:
                    res = ""
                    res += chr(ord('a') + j)
                    res += str(8-i)
                    ret.append(res)
                elif arr[i][j] >= "1" and arr[i][j] <= "9":
                    j += ord(arr[i][j]) - ord('0')
        return ret

    def get_list_moves(self, sboard):
        board = chess.Board(sboard)        
        self._engine.position(board)
        res = list()
        moves = board.legal_moves
        for move in moves:
            self._engine.go(searchmoves=[move], depth=self._depth)
            scr = self._info_handler.info['score'][1].cp
            mate = self._info_handler.info['score'][1].mate
            if mate == 1:
                scrf = self._scrf
            elif mate == -1:
                continue 
            elif scr != None:
                scrf = round(float(scr)/1000, 2)
            res.append({'move' : move.uci(), 'score' : scrf})
        res.sort(key=lambda p:-p['score'])
        reslist = []
        for el in res:
            reslist.append(self.convert_move(el))     
        return reslist

    def get_list_figures_uci(self, sboard):
        board = chess.Board(sboard)        
        self._engine.position(board)
        res = list()
        moves = board.legal_moves
        for move in moves:
            self._engine.go(searchmoves=[move], depth=self._depth)
            scr = self._info_handler.info['score'][1].cp
            mate = self._info_handler.info['score'][1].mate
            if mate == 1:
                scrf = self._scrf
            elif mate == -1:
                continue 
            elif scr != None:
                scrf = round(float(scr)/1000, 2)
            res.append({'move' : move.uci(), 'score' : scrf})
        res.sort(key=lambda p:-p['score'])
        reslist = []
        for el in res:
            reslist.append(el["move"][0:2])     
        return reslist

    def get_list_moves_uci(self, sboard):
        board = chess.Board(sboard)        
        self._engine.position(board)
        res = list()
        moves = board.legal_moves
        for move in moves:
            self._engine.go(searchmoves=[move], depth=self._depth)
            scr = self._info_handler.info['score'][1].cp
            mate = self._info_handler.info['score'][1].mate
            if mate == 1:
                scrf = self._scrf
            elif mate == -1:
                continue 
            elif scr != None:
                scrf = round(float(scr)/1000, 2)
            res.append({'move' : move.uci(), 'score' : scrf})
        res.sort(key=lambda p:-p['score'])
        reslist = []
        for el in res:
            reslist.append(el["move"])     
        return reslist
    
    def how_best_move(self, sboard):
        board = chess.Board(sboard)        
        self._engine.position(board)
        res = list()
        moves = board.legal_moves
        for move in moves:
            self._engine.go(searchmoves=[move], depth=self._depth)
            scr = self._info_handler.info['score'][1].cp
            mate = self._info_handler.info['score'][1].mate
            if mate == 1:
                scrf = self._scrf
            elif mate == -1:
                continue
            elif mate == -2:
                scr = -5
            elif scr != None:
                scrf = round(float(scr)/1000, 2)
            res.append({'move' : move, 'score' : scrf})
        res.sort(key=lambda p:-p['score'])
        if res.__len__() == 0:
            return None
        bestmove = res[0]['move']
        status = self._ustate
        r ='RK'
        san = board.san(bestmove)
        castling = 0
        for c in san:
            if c == 'O':
                castling = castling + 1
        if castling == 2:
            status = self._shstate
        elif castling == 3:
            status = self._lnstate
        else:   
            for c in ['a','b','c','d','e','f','g','h']:
                if san[0] == c:
                    r = 'P'
            if r != 'P':
                r = san[0]
            if res[0]['score'] == self._scrf:
                status = self._mstate
            else:
                for c in san:
                    if c == 'x':
                        status = self._estate
                for c in san:
                    if c == '+':
                        if status == self._estate:
                            status = self._eastate
                        else:
                            status = self._astate
            
        return [self.convert_move({'move':bestmove.uci()}), r, status, bestmove.uci()]

class CheckFunc:
    
    _nstat = 0
    _sstat = 1
    _mstat = 2
    _pstat = 3

    def check_castling(self, sboard):
        board = chess.Board(sboard)
        notate = sboard.split(' ')[2]
        req1 = {'K':False, 'Q':False}
        for c in notate:
            req1[c]=True
        if not (req1['K'] or req1['Q']):
            return None
        req2 = {'K':False, 'Q':False}
        for move in board.legal_moves:
            if 'e1c1'==move.uci():
                req2['K'] = True
            elif 'e1g1'==move.uci():
                req2['Q'] = True
        reslist = list()
        if req1['K'] and req2['K']:
             reslist.append([[4, 0], [0, 0]])
        if req1['Q'] and req2['Q']:
             reslist.append([[4, 0], [7, 0]])
        return reslist

    def get_crit(self, sboard):
        figures = sboard.split(' ')[0]
        white = 0.0
        black = 0.0
        for ch in figures:
            if ch == 'R':
                white = white + 5
            elif ch == 'r':
                black = black + 5
            elif ch == 'N':
                white = white + 3
            elif ch == 'n':
                black = black + 3
            elif ch == 'B':
                white = white + 3.5
            elif ch == 'b':
                black = black + 3.5
            elif ch == 'Q':
                white = white + 10
            elif ch == 'q':
                black = black + 10
            elif ch == 'K':
                white = white + 4
            elif ch == 'k':
                black = black + 4
            elif ch == 'P':
                white = white + 1
            elif ch == 'p':
                black = black + 1
        return [white, black]

    def check_state(self, sboard):
        board = chess.Board(sboard)
        if board.legal_moves.count == 0:
            return self._pstat
        if board.is_game_over():
            return self._mstat
        if board.is_check():
            return self._sstat
        return self._nstat
    
    def upd_fen(self, sboard, sturn):
        board = chess.Board(sboard)
        board.push(chess.Move.from_uci(sturn))
        return board.fen()

# obj = MovesFinder()
# res = obj.find_figure("rnbqkbnr/6N1/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1", "N")
# print(res)
# print(obj.get_list_figures_uci("rnbqkbnr/6N1/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"))
# print(obj.find_figure_moves("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2", "N"))