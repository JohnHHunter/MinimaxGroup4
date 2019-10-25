from player4.reversi_players import *

def get_default_player(symbol):
    """
    :returns: a default minimax player that can operate successfully on a given 8x8 board
    """
    return MinimaxPlayer(symbol)


def get_player_a(symbol):
    """
    :author: Josh Hayden
    :enchancement: Advanced Evaluation Functions
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return NoOpponentCornersPlayer(symbol)


def get_player_b(symbol):
    """
    :author: Tea Mdevadze
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return AlphaBetaPlayer(symbol)


def get_player_c(symbol):
    """
    :author: Timothy Marotta
    :enchancement: Transposition Table
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MinimaxTranspositionPlayer(symbol)


def get_player_d(symbol):
    """
    :author: John Hunter
    :enchancement: Incoperates random moves to take down deterministic foes
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MinimaxRandomPlayer(symbol)


def get_combined_player(symbol):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
    return CombinedPlayer(symbol)
