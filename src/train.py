import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__)))

import logging

from tic_tac_toe import Game
from tic_tac_toe.players import HumanPlayer, RandomPlayer

from training import Trainer

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    game = Game()
    player_one = RandomPlayer(name='One')
    player_two = RandomPlayer(name='Two')
    Trainer.train(iterations=2, plays=10000, game=game, players=[player_one, player_two])
