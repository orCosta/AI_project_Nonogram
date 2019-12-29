# AI_FinalProj
![image](https://user-images.githubusercontent.com/44048156/71555141-26be6f00-2a31-11ea-8baf-0052df358439.png)


The project contains the next files:

NonogramProblem.py:
Contains implementation of 3 kinds of problems, 1st with filling cell approach, the 2nd with the row/col approach and the 3rd with row/col and heuristic method.  In addition, there is different searching function that use different methods.

Board.py:
class for the game representation, the board contains a matrix that represent the grid and lists with the row and col conditions. The class also contains the implementation of the method that used by the searching funcs.

Nono_runner.py:
Runs the main function that get game and solve it. The runner can read the board configuration from a Json file with same format that can be found in externals. The runner should run from the Cmd, you should run ”>>python nono_runner.py –h “ for more info.

Display.py:
contains the function that print the board and some more.
