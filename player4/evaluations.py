
def spacesControlled(board, symbol):
    scores = board.calc_scores()

    return scores[symbol]

def spacesControlledDifference(board, symbol):
    yourScore = spacesControlled(board, symbol)
    oppScore = spacesControlled(board, changeSymbol(symbol))
    return yourScore - oppScore


def weightedEdges(board, symbol, weight):
    score = 0
    for x in range(board.get_size()):
        for y in range(board.get_size()):
            if board.get_symbol_for_position((x, y)) == symbol:
                if (x == 0 and y == 0) or (x == board.get_size() - 1 and y == board.get_size() - 1):
                    score += (weight * weight)
                elif x == 0 or y == 0 or x == board.get_size() - 1 or y == board.get_size() - 1:
                    score += weight
                else:
                    score += 1
    return score


def justCorners(board, symbol, weight):
    score = 0
    for x in range(board.get_size()):
        for y in range(board.get_size()):
            if board.get_symbol_for_position((x, y)) == symbol:
                if (x == 0 and y == 0) or (x == board.get_size() - 1 and y == board.get_size() - 1):
                    score += weight
                else:
                    score += 1
    return score

def weightedEdgesDifference(board, symbol, weight):
    yourScore = weightedEdges(board, symbol, weight)
    oppScore = weightedEdges(board, changeSymbol(symbol), weight)
    return yourScore - oppScore


# This method works best, beats minimax with weighted edges as well as minimax with spaces controlled.
# Beat random computer player 807 times out of 1000, lost 170 and tied 23
# def noOpponentCorners(board, symbol):
#     score = 0
#     for x in range(board.get_size()):
#         for y in range(board.get_size()):
#             if board.get_symbol_for_position((x, y)) == symbol:
#                     score += 1
#             elif board.get_symbol_for_position((x, y)) == changeSymbol(symbol):
#                 if (x == 0 and y == 0) or (x == board.get_size() - 1 and y == board.get_size() - 1):
#                     return 0
#
#     return score

def noOpponentCorners(board, symbol):
    score = 0
    scale = board.get_size() * board.get_size()
    otherSymbol = changeSymbol(symbol)
    for x in range(board.get_size()):
        for y in range(board.get_size()):
            if board.get_symbol_for_position((x, y)) == symbol:
                    score += 1
            elif board.get_symbol_for_position((x, y)) == otherSymbol:
                if (x == 0 and y == 0) or (x == board.get_size() - 1 and y == board.get_size() - 1):
                    score -= scale

    return score


# Should weight controlling a 'triangle' out of a corner as more desirable, once you do this the opponent can't take a triangle back

def triangleControl(board, symbol):
    score = 0

    return score


# If all edges are occupied treat next level in as new edges/corners.
def workInEdges(board, symbol):
    score = 0
    return score


def changeSymbol(symbol):
    if symbol == 'X':
        return 'O'
    else:
        return 'X'