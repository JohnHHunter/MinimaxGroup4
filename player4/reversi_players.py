# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license:
# https://inventwithpython.com/#donate
import random
import copy
from math import inf
from player4.evaluations import *
import time


class HumanPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        valid_digits = []
        for i in range(1, board.get_size() + 1):
            valid_digits.append(str(i))
        no_valid_move = True
        while no_valid_move:
            move = input(self.symbol + ', enter your move:').lower()
            if len(move) == 2 and move[0] in valid_digits and move[1] in valid_digits:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if board.is_valid_move(self.symbol, (x, y)):
                    no_valid_move = False
                    return [x, y]
                else:
                    print('Not a valid move.')
            else:
                print('Bad input. Type valid x digit, then the y digit.')


class RandomComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        return random.choice(board.calc_valid_moves(self.symbol))


class GreedyComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        all_valid_moves = board.calc_valid_moves(self.symbol)
        best_move = (board, 0, None)
        for x in all_valid_moves:

            # make a copy of the board
            new_board = copy.deepcopy(board)

            # make a move on the board
            new_board.make_move(self.symbol, x)

            # get the score of the new board
            new_score = new_board.calc_scores()[self.symbol]

            # if the score is better, save it
            if new_score > best_move[1]:
                best_move = (new_board, new_score, x)

        return best_move[2]

    
class MinimaxRandomPlayer:
    def __init__(self, symbol):
        self.symbol = symbol
        random.seed(112342)

    def get_move(self, board):
        if random.randint(1, 8) is 1:
            return random.choice(board.calc_valid_moves(self.symbol))
        if len(board.calc_valid_moves(self.symbol)) == 1:
            return board.calc_valid_moves(self.symbol)[0]
        answer = minimax(board, 2, self.symbol, True)[:2]
        return answer[0], answer[1]

    
class AlphaBetaPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        if len(board.calc_valid_moves(self.symbol)) == 1:
            return board.calc_valid_moves(self.symbol)[0]
        answer = AlphaBeta(board, 2, self.symbol)
        # print(answer)
        return answer[0], answer[1]


def AlphaBeta(board, depth, symbol):
    def max_value(board, alpha, beta, symbol, depth):
        if not board.game_continues():
            return [-1, -1, endgameUtility(board, symbol)]

        elif depth == 0 or len(board.calc_valid_moves(symbol)) == 0:
            return [-1, -1, utility(board, symbol)]
        best = [-1, -1, -inf]


        for move in board.calc_valid_moves(symbol):
            copied_board = copy.deepcopy(board)
            copied_board.make_move(symbol, move)
            score = min_value(copied_board, alpha, beta, flipSymbol(symbol), depth - 1)
            if best[2] < score[2]:
                best[2] = score[2]
                best[0], best[1] = move[0], move[1]
            if best[2] >= beta:
                return best
            alpha = max(alpha, best[2])
        return best

    def min_value(board, alpha, beta, symbol, depth):
        if not board.game_continues():
            return [-1, -1, endgameUtility(board, symbol)]
        elif depth == 0 or len(board.calc_valid_moves(symbol)) == 0:
            return [-1, -1, utility(board, symbol)]

        best = [-1, -1, inf]

        for move in board.calc_valid_moves(symbol):
            copied_board = copy.deepcopy(board)
            copied_board.make_move(symbol, move)
            score = max_value(copied_board, alpha, beta, flipSymbol(symbol), depth - 1)
            if best[2] > score[2]:
                best[2] = score[2]
                best[0], best[1] = move[0], move[1]
            if best[2] <= alpha:
                return best
            beta = min(beta, best[2])
        return best

    return max_value(board, -inf, inf, symbol, depth)


class MinimaxPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        if len(board.calc_valid_moves(self.symbol)) == 1:
            return board.calc_valid_moves(self.symbol)[0]
        answer = minimax(board, 2, self.symbol, True)[:2]
        return answer[0], answer[1]


class NoOpponentCornersPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        start = time.time()

        if len(board.calc_valid_moves(self.symbol)) == 1:
            return board.calc_valid_moves(self.symbol)[0]
        answer = minimax2(board, 2, self.symbol, True)[:2]
        end = time.time()
        dif = end - start
        if (dif > 2.7):
            print("Time limit reached, time = " + dif)
        return answer[0], answer[1]


# weight for testing corner thing, can be whatever otherwise

class MinimaxTranspositionPlayer:

    def __init__(self, symbol):
        self.symbol = symbol
        self.transposition_table = {}

    def get_move(self, board):

        if len(board.calc_valid_moves(self.symbol)) == 1:
            return board.calc_valid_moves(self.symbol)[0]
        answer = self.minimax(board, 2, self.symbol, True)[:2]
        return answer[0], answer[1]

    def check_transposition_table(self, board, symbol):
        # @TODO should in statement actually be .get attempt? O(N) vs O(1)
        rot_original = board._board

        # check original board
        rot_original_hash = hash(str(rot_original))
        if rot_original_hash in self.transposition_table:
            return self.transposition_table.get(rot_original_hash)

        # rotate board 90 degrees
        rot_90 = list(zip(*reversed(copy.deepcopy(rot_original))))
        rot_90_hash = hash(str(rot_90))
        if rot_90_hash in self.transposition_table:
            return self.transposition_table.get(rot_90_hash)

        # rotate board 180 degrees
        rot_180 = list(zip(*reversed(copy.deepcopy(rot_90))))
        rot_180_hash = hash(str(rot_180))
        if rot_180_hash in self.transposition_table:
            return self.transposition_table.get(rot_180_hash)

        # rotate board 270 degrees
        rot_270 = list(zip(*reversed(copy.deepcopy(rot_180))))
        rot_270_hash = hash(str(rot_270))
        if rot_270_hash in self.transposition_table:
            return self.transposition_table.get(rot_270_hash)

        # add rot_original to table (not found otherwise)
        score = self.utility(board, symbol)
        self.transposition_table[rot_original_hash] = score
        return score

    def minimax(self, board, depth, symbol, max_depth):
        if max_depth:
            best = [-1, -1, -inf]
        else:
            best = [-1, -1, inf]

        if not board.game_continues():
            return [-1, -1, self.endgameUtility(board, symbol)]
        elif depth == 0 or len(board.calc_valid_moves(symbol)) == 0:
            return [-1, -1, self.check_transposition_table(board, symbol)]

        for move in board.calc_valid_moves(symbol):
            base_board = copy.deepcopy(board)
            base_board.make_move(symbol, move)
            score = self.minimax(base_board, depth - 1, self.flipSymbol(symbol), not max_depth)
            score[0], score[1] = move[0], move[1]

            if max_depth:
                if score[2] > best[2]:
                    best = score

            else:
                if score[2] < best[2]:
                    best = score

        return best

    def endgameUtility(self, board, symbol):
        return spacesControlled(board, symbol)

    def utility(self, board, symbol):
        return spacesControlled(board, symbol)

    def flipSymbol(self, symbol):
        if symbol == 'X':
            return 'O'
        else:
            return 'X'


def minimax2(board, depth, symbol, max):
    if max:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]

    if (not board.game_continues()):
        return [-1, -1, endgameUtility(board, symbol)]

    elif depth == 0 or len(board.calc_valid_moves(symbol)) == 0:
        return [-1, -1, utility2(board, symbol)]

    for move in board.calc_valid_moves(symbol):
        baseBoard = copy.deepcopy(board)
        baseBoard.make_move(symbol, move)
        score = minimax2(baseBoard, depth - 1, flipSymbol(symbol), not max)
        score[0], score[1] = move[0], move[1]

        if max:
            if score[2] > best[2]:
                best = score

        else:
            if score[2] < best[2]:
                best = score

    return best


def minimax(board, depth, symbol, max):
    if max:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]

    if (not board.game_continues()):
        return [-1, -1, endgameUtility(board, symbol)]

    elif depth == 0 or len(board.calc_valid_moves(symbol)) == 0:
        return [-1, -1, utility(board, symbol)]
    for move in board.calc_valid_moves(symbol):
        baseBoard = copy.deepcopy(board)
        baseBoard.make_move(symbol, move)
        score = minimax(baseBoard, depth - 1, flipSymbol(symbol), not max)
        score[0], score[1] = move[0], move[1]

        if max:
            if score[2] > best[2]:
                best = score

        else:
            if score[2] < best[2]:
                best = score

    return best


def endgameUtility(board, symbol):
    return spacesControlled(board, symbol)


def utility(board, symbol):
    return spacesControlled(board, symbol)


def utility2(board, symbol):
    return noOpponentCorners(board, symbol)


def flipSymbol(symbol):
    if symbol == 'X':
        return 'O'
    else:
        return 'X'


class CombinedPlayer:

    def __init__(self, symbol):
        self.symbol = symbol
        self.transposition_table = {}

    def get_move(self, board):
        # #Sneaky move is the next 4 lines, comment out if testing
        scores = board.calc_scores()
        combined = scores["X"] + scores["O"]
        if (combined == 4):
            time.sleep(3)
        if len(board.calc_valid_moves(self.symbol)) == 1:
            return board.calc_valid_moves(self.symbol)[0]
        answer = AlphaBeta(board, 4, self.symbol)
        return answer[0], answer[1]

    def AlphaBeta(board, depth, symbol):
        def max_value(board, alpha, beta, symbol, depth):
            if not board.game_continues():
                return [-1, -1, endgameUtility(board, symbol)]

            elif depth == 0 or len(board.calc_valid_moves(symbol)) == 0:
                return [-1, -1, utility(board, symbol)]
            best = [-1, -1, -inf]

            for move in board.calc_valid_moves(symbol):
                copied_board = copy.deepcopy(board)
                copied_board.make_move(symbol, move)
                score = min_value(copied_board, alpha, beta, flipSymbol(symbol), depth - 1)
                if best[2] < score[2]:
                    best[2] = score[2]
                    best[0], best[1] = move[0], move[1]
                if best[2] >= beta:
                    return best
                alpha = max(alpha, best[2])
            return best

        def min_value(board, alpha, beta, symbol, depth):
            if not board.game_continues():
                return [-1, -1, endgameUtility(board, symbol)]
            elif depth == 0 or len(board.calc_valid_moves(symbol)) == 0:
                return [-1, -1, utility(board, symbol)]

            best = [-1, -1, inf]

            for move in board.calc_valid_moves(symbol):
                copied_board = copy.deepcopy(board)
                copied_board.make_move(symbol, move)
                score = max_value(copied_board, alpha, beta, flipSymbol(symbol), depth - 1)
                if best[2] > score[2]:
                    best[2] = score[2]
                    best[0], best[1] = move[0], move[1]
                if best[2] <= alpha:
                    return best
                beta = min(beta, best[2])
            return best

        return max_value(board, -inf, inf, symbol, depth)

        def utility(board, symbol):
            return NoOpponentCornersPlayer(board, symbol)

        def endgameUtility(board, symbol):
            return spacesControlled(board, symbol)
