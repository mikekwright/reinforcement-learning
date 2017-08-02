Reinforcement Learning
============================================================

A simple repository that contains the different algorithms and implementations that I have
created while going over reinforcement learning and some different algorithms.

## Chapter 1

There is a `tic-tac-toe` problem that basically works by following a simple pattern of
creating a value for a board and then adjusting the value based on a step value with
an exploratory option.

    V(s) = V(s) - step*(V(s) - V(s'))
