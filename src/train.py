import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__)))

import logging

from tic_tac_toe import Game
from tic_tac_toe.players import MinMaxPlayer, RandomPlayer, FirstTrainedPlayer

from training import Trainer

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    game = Game()
    player_one = FirstTrainedPlayer(name='One')
    # player_two = MinMaxPlayer(name='Two', make_imperfect=True)
    # player_two = FirstTrainedPlayer(name='Two')
    player_two = RandomPlayer(name='Two')
    Trainer.train(iterations=10, plays=10000, game=game, players=[player_one, player_two], rotate_players=True)
    player_one.store_state(os.path.join(os.path.dirname(__file__), 'state', 'first_trained_state.json'))
