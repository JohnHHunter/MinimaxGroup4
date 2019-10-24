# MinimaxGroup4

**Josh Hayden:** Added the evaluation methods and made the NoOpponentCornersPlayer. This method worked best out of all the ones I tested.
It beat spacesControlled as well as weighting corners and edges or just corners every time. Minimax using this evaluation method, with a depth of 2, beat random 80% of the time.

**Tim Marotta:** Added the MinimaxTranspositionPlayer. This transposition table takes more time than a regular minimax on a 4x4 board each set to look ahead to depth at 4, but always wins against a regular minimax agent. Against a random agent, transposition table minimax wins 90% of the time.

**Tea Mdevadze:** Added the AlphaBetaPruning. AlphaBetaPruning is version of Minimax that is more efficient. It was tested on 8x8 board it takes almost 10 times less than regular minimax. It wins over random and greedy agents, it wins as many games as minimax when compared to it.

**John Hunter** Pair programmed with Tim on the Transposition Table. Also implemented the MinimaxRandomPlayer, which is a mix of the RandomPlayer and the standard MinimaxPlayer. The randomness of this agent disrupts the plans of deterministic minimax agents who expect their oppoenent to make optimal moves. This player has been demonstrated to reduce time significantly, which would be especially helpful in time-bank gameplay. Currently the improvement of gameplay is uncomfirmed do to issues with the compare_players function. A possible improvement for this agent is a quiescence hueristic, which could help the agent choose when to make a random move at the least risky times.
