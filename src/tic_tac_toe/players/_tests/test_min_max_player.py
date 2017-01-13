import logging
import sys

from board import Board
from players.min_max_player import MinMaxPlayer

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


def test_min_max_selects_correct_move():
    b = Board()
    test_model = MinMaxPlayer()
    b.board = [2, 1, 0,
               0, 1, 0,
               0, 0, 2]
    expected_move = 6

    test_model.start_game(player_num=1)
    actual_move = test_model.make_move(b)
    assert actual_move == expected_move
