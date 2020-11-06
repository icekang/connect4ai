# Connect4AI
## How it works
AI implements Minimax with Alpha–beta pruning. <br>
In order to overcome the resource limitation, it also implements Dynamic cut-off which limit the maximun depth of state space search. With this it also uses heuristic function, <strong>magic_score</strong> that simply sums the square of all counts of consecutive chips of each direction divided by sum of that of the opponent's. <br>
## How to use
To play with game UI which I excerped from https://github.com/KeithGalli/Connect4-Python <br>
run ``python connect4game.py``<br>
Simply run ``python connect4ai.py`` and you are good to go.<br>
I know that this is not perfect. If you have any suggestion, please tell me!
