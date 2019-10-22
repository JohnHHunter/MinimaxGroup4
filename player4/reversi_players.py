# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license:
# https://inventwithpython.com/#donate
import random
import copy
from math import inf
from player4.evaluations import spacesControlled, weightedEdges


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
        self.transposition_table = {}

    def get_move(self, board):

        if len(board.calc_valid_moves(self.symbol)) == 1:
            return board.calc_valid_moves(self.symbol)[0]
        answer = self.minimax(board, 4, self.symbol, True)[:2]
        return answer[0], answer[1]

    def check_transposition_table(self, board, symbol):
        # @TODO convert board to accessible 2d array
        rot_original = []
        for row in range(board.get_size()):
            row_holder = []
            rot_original.append(row_holder)
            for column in range(board.get_size()):
                rot_original[row][column] = board.get_symbol_for_position([row, column])

        # check original board
        rot_original_hash = hash(rot_original)
        if rot_original_hash in self.transposition_table:
            return self.transposition_table.get(rot_original_hash)

        # rotate board 90 degrees
        rot_90 = list(zip(*reversed(copy.deepcopy(rot_original))))
        rot_90_hash = hash(rot_90)
        if rot_90_hash in self.transposition_table:
            return self.transposition_table.get(rot_90_hash)

        # rotate board 180 degrees
        rot_180 = list(zip(*reversed(copy.deepcopy(rot_90))))
        rot_180_hash = hash(rot_180)
        if rot_180_hash in self.transposition_table:
            return self.transposition_table.get(rot_180_hash)

        # rotate board 270 degrees
        rot_270 = list(zip(*reversed(copy.deepcopy(rot_180))))
        rot_270_hash = hash(rot_270)
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

        return weightedEdges(board, symbol)

    def flipSymbol(self, symbol):
        if symbol == 'X':
            return 'O'
        else:
            return 'X'
