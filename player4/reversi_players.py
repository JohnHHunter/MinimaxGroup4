# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy

# John Hunter

class HumanPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        valid_digits = []
        for i in range(1, board.get_size()+1):
            valid_digits.append(str(i))
        no_valid_move = True
        while no_valid_move:
            move = input(self.symbol + ', enter your move:').lower()
            if len(move) == 2 and move[0] in valid_digits and move[1] in valid_digits:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if board.is_valid_move(self.symbol, ( x, y) ):
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


# With the current implementation, minimax must be 'X'
class MinimaxComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        move = minimax(board, 5, True)[0]
        return move


def minimax(board, depth, my_turn):

    if my_turn:
        best = [(0, 0), -999]
        symbol = 'X'
    else:  # opponents turn
        best = [(0, 0), 999]
        symbol = 'O'

    # break case
    if depth == 0 or not board.game_continues():
        end_scores = board.calc_scores()
        if end_scores['X'] > end_scores['O']:
            return [None, 1]
        if end_scores['X'] < end_scores['O']:
            return [None, -1]
        else:
            # tie game
            return [None, 0]

    for move in board.calc_valid_moves(symbol):
        # set up possible board
        new_board = copy.deepcopy(board)
        new_board.make_move(symbol, move)
        score = minimax(new_board, depth-1, not my_turn)
        score[0] = move

        if score[1] == 999 or score[1] == -999:
             score[1] = -1

        # compare the results of the possible board
        if my_turn:
            if score[1] > best[1]:
                best = score
        else:
            if score[1] < best[1]:
                best = score

    return best

# def minimax(board, depth, symbol, max):
#     if max == True:
#         best = [-1, -1, -inf]
#     else:
#         best = [-1, -1, inf]
#
#     if (depth == 0 or len(board.calc_valid_moves(symbol)) == 0):
#
#         return [-1, -1, utility(board, symbol)]
#
#     for move in board.calc_valid_moves(symbol):
#         baseBoard = copy.deepcopy(board)
#         baseBoard.make_move(symbol, move)
#         score = minimax(baseBoard, depth - 1, flipSymbol(symbol), not max)
#         score[0], score[1] = move[0], move[1]
#
#         if max == True:
#             if score[2] > best[2]:
#                 best = score
#
#         else:
#             if score[2] < best[2]:
#                 best = score
#
#
#
#
#     return best
#
#
# def basicUtility(board, symbol):
#     scores = board.calc_scores()
#
#     return scores[symbol]
#
#
# def utility(board, symbol):
#     score = 0
#     for x in range(board.get_size()):
#         for y in range(board.get_size()):
#             if board.get_symbol_for_position((x, y)) == symbol:
#                 if ((x == 0 and y == 0) or (x == board.get_size() - 1 and y == board.get_size() - 1)):
#                     score += 100
#                 elif (x == 0 or y == 0 or x == board.get_size() - 1 or y == board.get_size() - 1):
#                     score += 10
#                 else:
#                     score += 1
#     return score
#
# def flipSymbol(symbol):
#     if symbol == 'X':
#         return 'O'
#     else:
#         return 'X'
#
# class Player:
#     def __init__(self, symbol):
#         self.symbol = symbol
#
#     # def evaluate(self, board, player):
#     #     if player == "MAX":
#     #         scores = board.calc_scores()
#     #         diff = scores[self.symbol] - scores[board.get_opponent_symbol(self.symbol)]
#     #     else:
#     #         scores = board.calc_scores()
#     #         diff = scores[board.get_opponent_symbol(self.symbol)] - scores[self.symbol]
#     #
#     #     return int(diff)
#     def evaluate(self, board):
#         scores = board.calc_scores()
#         diff = scores[self.symbol] - scores[board.get_opponent_symbol(self.symbol)]
#         return int(diff)
#
#     def minimax(self, board, depth, player):
#         if player == "MAX":
#             current_symbol = self.symbol
#             best = [-1, -1, -infinity]
#         else:
#             current_symbol = board.get_opponent_symbol(self.symbol)
#             best = [-1, -1, +infinity]
#
#         if depth == 0 or board.calc_valid_moves(current_symbol) == []:
#             score = self.evaluate(board)
#             return [-1, -1, score]
#         for i in board.calc_valid_moves(current_symbol):
#             copied_board = copy.deepcopy(board)
#             x, y = i[0], i[1]
#             if player == "MAX":
#                 copied_board.make_move(self.symbol, i)
#                 score = self.minimax(copied_board, depth - 1, "MIN")
#             else:
#                 copied_board.make_move(copied_board.get_opponent_symbol(self.symbol), i)
#                 score = self.minimax(copied_board, depth - 1, "MAX")
#             score[0], score[1] = x, y
#
#             if player == "MAX":
#                 if score[2] > best[2]:
#                     best = score  # max value
#             else:
#                 if score[2] < best[2]:
#                     best = score  # min value
#         return best
#
#     def get_move(self, board):
#         if len(board.calc_valid_moves(self.symbol)) == 1:
#             return board.calc_valid_moves(self.symbol)[0]
#         move = self.minimax(board, 4, "MAX")
#         return [move[0], move[1]]
