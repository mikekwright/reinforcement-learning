import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__)))

import logging

from tic_tac_toe import Game
from tic_tac_toe.players import HumanPlayer, RandomPlayer, MinMaxPlayer

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    game = Game()
    player_one = HumanPlayer()
    # player_two = RandomPlayer()
    player_two = MinMaxPlayer()
    game.play(players=[player_one, player_two])
