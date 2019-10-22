# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license:
# https://inventwithpython.com/#donate
import random
import copy
from math import inf
from evaluations import spacesControlled, weightedEdges, spacesControlledDifference, weightedEdgesDifference, justCorners, noOpponentCorners


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


class MinimaxPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        if len(board.calc_valid_moves(self.symbol)) == 1:
            return board.calc_valid_moves(self.symbol)[0]
        answer = minimax(board, 2, self.symbol, True)[:2]
        return answer[0], answer[1]


class MinimaxPlayer2:

    def __init__(self, symbol, weight):
        self.symbol = symbol
        self.weight = weight

    def get_move(self, board):
        if len(board.calc_valid_moves(self.symbol)) == 1:
            return board.calc_valid_moves(self.symbol)[0]
        answer = minimax2(board, 2, self.symbol, True, self.weight)[:2]
        return answer[0], answer[1]
## weight for testing corner thing, can be whatever otherwise

def minimax2(board, depth, symbol, max, weight):
    if max:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]

    if (not board.game_continues()):
        return [-1, -1, endgameUtility(board, symbol)]

    elif depth == 0 or len(board.calc_valid_moves(symbol)) == 0:
        return [-1, -1, utility2(board, symbol, weight)]


    for move in board.calc_valid_moves(symbol):
        baseBoard = copy.deepcopy(board)
        baseBoard.make_move(symbol, move)
        score = minimax2(baseBoard, depth - 1, flipSymbol(symbol), not max, weight)
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

    return noOpponentCorners(board, symbol)



def utility2(board, symbol, weight):

    return noOpponentCorners(board, symbol, weight)


def flipSymbol(symbol):
    if symbol == 'X':
        return 'O'
    else:
        return 'X'
