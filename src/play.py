import os
import sys
import logging

sys.path.append(os.path.join(os.path.dirname(__file__)))

from tic_tac_toe import Game
from tic_tac_toe.players import HumanPlayer, MinMaxPlayer, FirstTrainedPlayer, RandomPlayer, ValueTrainedPlayer


def play_human_player_two():
    game = Game()
    player_one = MinMaxPlayer()
    player_two = HumanPlayer()
    game.play(players=[player_one, player_two])


def play_human_player_one():
    game = Game()
    player_one = HumanPlayer()
    # player_two = MinMaxPlayer(make_imperfect=True)
    player_two = MinMaxPlayer(make_imperfect=False)
    game.play(players=[player_one, player_two])


def play_human_and_first_trained():
    game = Game()
    player_one = FirstTrainedPlayer()
    player_one.load_state(os.path.join(os.path.dirname(__file__), 'state', 'first_trained_state.json'))
    player_two = HumanPlayer()
    # player_two = RandomPlayer()
    game.play(players=[player_one, player_two])


def play_human_and_value_trained():
    game = Game()
    player_one = HumanPlayer(name='Me')
    player_two = ValueTrainedPlayer(name='two', exploratory_percent=0)
    # player_two.load_state(os.path.join(os.path.dirname(__file__), 'state', 'value_trained_itself_state.json'))
    player_two.load_state(os.path.join(os.path.dirname(__file__), 'state', 'value_trained_minmax_state.json'))
    game.play(players=[player_one, player_two])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # play_human_player_one()
    # play_human_player_two()
    # play_human_and_first_trained()
    play_human_and_value_trained()