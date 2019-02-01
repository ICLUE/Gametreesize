# Gametreesize
Code for the paper "An estimation method for game complexity"

Alexander Yong and David Yong

https://arxiv.org/abs/1901.11161

Usage Instructions
----------

This repository contains three python estimators for estimating game tree sizes
* `tictactoe.v0.1.py` estimates the game tree size of tic tac toe (this is already known exactly)
* `connectfour.v0.1.py` does the same for Connect Four
* `Othello.v0.1.py` applies to Othello (the modern version of Reversi), with the standard rules that the center
squares are occupied in the opening.

Sample usage is as follows

```
python tictactoe.v0.1.py 
Sample size : 2000 
Number of processor cores to use (0 if you want to use all) : 0
('Sample size; cores used', 2000, 0)
--------------------------------------
            RESULTS                   
--------------------------------------
('* Estimated number of games of Tic Tac Toe is', 256238.64)
('* Estimated average game length is ', 8.246474302236383)
('* Estimated percentage of first player wins is ', 0.5087036053578804)
('* Estimated percentage of second player wins is ', 0.29940402431108754)
('* Estimated percentage of draws is ', 0.19189237033103201)
('Executed in seconds: ', 0.4519460201263428)
```
