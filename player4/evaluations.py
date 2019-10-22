def spacesControlled(board, symbol):
    scores = board.calc_scores()

    return scores[symbol]


def weightedEdges(board, symbol):
    score = 0
    for x in range(board.get_size()):
        for y in range(board.get_size()):
            if board.get_symbol_for_position((x, y)) == symbol:
                if (x == 0 and y == 0) or (x == board.get_size() - 1 and y == board.get_size() - 1):
                    score += 100
                elif x == 0 or y == 0 or x == board.get_size() - 1 or y == board.get_size() - 1:
                    score += 10
                else:
                    score += 1
    return score


def triangleControl(board, symbol):
    score = 0

    return score