import json
from reversi_game import *


def main():
    # create objects to be reused
    combined = CombinedPlayer("X")
    base = MinimaxPlayer("O")
    rand = RandomComputerPlayer("O")

    compare_json_players(combined, base, 1001)
    compare_json_players(combined, rand, 100001)

    print()

if __name__ == "__main__":
    main()


def compare_json_players(player1, player2, num_games, board_size=8, board_filename=None):
    game_count_map = {player1.symbol: 0, player2.symbol: 0, "TIE": 0}
    time_elapsed_map = {player1.symbol: 0, player2.symbol: 0}
    for i in range(1, num_games):
        if i % 100 == 0:
            # pass
            print(i, "games finished")

        # swap who goes first
        if i % 2 == 0:
            game = ReversiGame(player1, player2, show_status=False, board_size=board_size,
                               board_filename=board_filename)
        else:
            game = ReversiGame(player2, player1, show_status=False, board_size=board_size,
                               board_filename=board_filename)

        game_count_map[game.calc_winner()] += 1
        decision_times = game.get_decision_times()
        for symbol in decision_times:
            time_elapsed_map[symbol] += decision_times[symbol]
    print(game_count_map)
    print(time_elapsed_map)
