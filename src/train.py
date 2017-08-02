import logging
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Have to set it before importing tensorflow or you lose all logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from logging import info

from tic_tac_toe import Game
from tic_tac_toe.players import FirstTrainedPlayer, HumanPlayer, RandomPlayer, MinMaxPlayer, ValueTrainedPlayer, SupervisedDeepPlayer

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


def train_first_trained_player_with_value():
    game = Game()
    player_one = FirstTrainedPlayer(name='One')
    player_two = ValueTrainedPlayer(name='Two')
    Trainer.train(iterations=10, plays=10000, game=game, players=[player_one, player_two], rotate_players=True)
    player_one.store_state(os.path.join(os.path.dirname(__file__), 'state', 'first_trained_valued_state.json'))
    player_two.store_state(os.path.join(os.path.dirname(__file__), 'state', 'value_trained_first_state.json'))


def train_value_trained_player_with_random():
    game = Game()
    player_one = ValueTrainedPlayer(name='One')
    player_two = RandomPlayer(name='Two')
    Trainer.train(iterations=10, plays=100000, game=game, players=[player_one, player_two], rotate_players=True)
    player_one.store_state(os.path.join(os.path.dirname(__file__), 'state', 'value_trained_random_state.json'))


def train_value_trained_player_with_itself():
    game = Game()
    player_one = ValueTrainedPlayer(name='One')
    player_two = ValueTrainedPlayer(name='Two')
    Trainer.train(iterations=2, plays=100000, game=game, players=[player_one, player_two], rotate_players=True)
    player_one.store_state(os.path.join(os.path.dirname(__file__), 'state', 'value_trained_itself_state.json'))


def train_value_trained_player_with_minmax():
    game = Game()
    player_one = ValueTrainedPlayer(name='One')
    player_two = MinMaxPlayer(name='Two', make_imperfect=True)
    Trainer.train(iterations=2, plays=100000, game=game, players=[player_one, player_two], rotate_players=True)
    player_one.store_state(os.path.join(os.path.dirname(__file__), 'state', 'value_trained_minmax_state.json'))


def train_value_trained_player_with_human():
    game = Game()
    player_one = ValueTrainedPlayer(name='One')
    player_two = HumanPlayer()
    Trainer.train(iterations=2, plays=10, game=game, players=[player_one, player_two], rotate_players=True)
    player_one.store_state(os.path.join(os.path.dirname(__file__), 'state', 'value_trained_human_state.json'))


def train_supervised_trained_with_random():
    game = Game()

    info('Training supervised with random 10000 times (as first and second player)')
    # player_one = SupervisedDeepPlayer(version='three_layer', train_size=10000)
    player_one = SupervisedDeepPlayer(version='two_layer', train_size=10000)
    player_two = RandomPlayer()
    Trainer.train(iterations=1, plays=50000, game=game, players=[player_one, player_two], rotate_players=True)
    player_one.store_state(os.path.join(os.path.dirname(__file__), 'state', 'supervised', 'two_layer', 'random_trained'))

    # info('Training supervised with imperfect min-max 10000 times (as first and second player)')
    # player_two = MinMaxPlayer(name='Two', make_imperfect=True, random_percent=.3)
    # Trainer.train(iterations=2, plays=10000, game=game, players=[player_one, player_two], rotate_players=True)
    # player_one.store_state(os.path.join(os.path.dirname(__file__), 'state', 'supervised', 'two_layer', 'minmax_trained'))


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)

    # First Trained Player Training
    # train_first_trained_player_with_itself()
    # train_first_trained_player_with_random()
    # train_first_trained_player_with_imperfect_min_max()
    # train_first_trained_player_with_value()

    # Value Trained Player Training
    # train_value_trained_player_with_random()
    # train_value_trained_player_with_itself()
    # train_value_trained_player_with_minmax()
    # train_value_trained_player_with_human()

    # Supervised Deep Player Training
    train_supervised_trained_with_random()

