import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cartpole import CartPoleGame

game = CartPoleGame()
game.train(passes=1000)

