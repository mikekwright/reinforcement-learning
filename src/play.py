import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__)))

import logging

from tic_tac_toe import Game
from tic_tac_toe.players import HumanPlayer, MinMaxPlayer


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


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    play_human_player_two()


