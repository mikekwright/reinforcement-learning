import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__)))

import logging

from tic_tac_toe import Game
from tic_tac_toe.players import MinMaxPlayer, RandomPlayer, FirstTrainedPlayer

from training import Trainer


def train_first_trained_player_with_random():
    game = Game()
    player_one = FirstTrainedPlayer(name='One')
    player_two = RandomPlayer(name='Two')
    Trainer.train(iterations=10, plays=10000, game=game, players=[player_one, player_two], rotate_players=True)
    player_one.store_state(os.path.join(os.path.dirname(__file__), 'state', 'first_trained_random_state.json'))


def train_first_trained_player_with_imperfect_min_max():
    game = Game()
    player_one = FirstTrainedPlayer(name='One')
    player_two = MinMaxPlayer(name='Two', make_imperfect=True)
    Trainer.train(iterations=2, plays=1000, game=game, players=[player_one, player_two], rotate_players=True)
    player_one.store_state(os.path.join(os.path.dirname(__file__), 'state', 'first_trained_minmax_state.json'))


def train_first_trained_player_with_itself():
    game = Game()
    player_one = FirstTrainedPlayer(name='One')
    player_two = FirstTrainedPlayer(name='Two')
    Trainer.train(iterations=10, plays=10000, game=game, players=[player_one, player_two], rotate_players=True)
    player_one.store_state(os.path.join(os.path.dirname(__file__), 'state', 'first_trained_itself_state.json'))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    train_first_trained_player_with_itself()
    # train_first_trained_player_with_random()
    # train_first_trained_player_with_imperfect_min_max()
