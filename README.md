# MinimaxGroup4

**Josh Hayden:** Added the evaluation methods and made the NoOpponentCornersPlayer. This method worked best out of all the ones I tested.
It beat spacesControlled as well as weighting corners and edges or just corners every time. Minimax using this evaluation method, with a depth of 2, beat random 80% of the time.

**Tim Marotta:** Added the MinimaxTranspositionPlayer. This transposition table takes more time than a regular minimax on a 4x4 board each set to look ahead to depth at 4, but always wins against a regular minimax agent. Against a random agent, transposition table minimax wins 90% of the time.
