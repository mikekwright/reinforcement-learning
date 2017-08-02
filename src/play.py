import os
import sys
import logging
from logging import debug, info
from collections import deque
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__)))

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
# logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from tic_tac_toe import Game
from tic_tac_toe.players import HumanPlayer, MinMaxPlayer, FirstTrainedPlayer, RandomPlayer, ValueTrainedPlayer, \
    SupervisedDeepPlayer


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


def play_value_vs_minmax_manytimes(times=1000):
    win, loss, draw = 0, 0, 0
    game = Game()
    # player_one = MinMaxPlayer(make_imperfect=True)
    player_one = MinMaxPlayer()
    player_two = ValueTrainedPlayer(name='two', exploratory_percent=0)
    player_two.load_state(os.path.join(os.path.dirname(__file__), 'state', 'value_trained_minmax_state.json'))

    for i in range(times):
        if i % 100 == 0:
            info('playing game {} of {} - loss {} draw {} win {}'.format(i, times, loss, draw, win))
        result = game.play(players=[player_one, player_two])
        if result == 0:
            draw += 1
        elif result == 1:
            loss += 1
        elif result == 2:
            win += 1

    info('Switching first and second players')
    for i in range(times):
        if i % 100 == 0:
            info('playing game {} of {} - loss {} draw {} win {}'.format(i, times, loss, draw, win))
        result = game.play(players=[player_two, player_one])
        if result == 0:
            draw += 1
        elif result == 1:
            win += 1
        elif result == 2:
            loss += 1


def play_human_vs_minmax():
    game = Game()
    player_one = HumanPlayer()
    player_two = MinMaxPlayer()
    while True:
        game.play(players=[player_one, player_two])


def play_two_layer_vs_human():
    game = Game()
    player_one = SupervisedDeepPlayer(version='two_layer')
    player_one.load_state(os.path.join(os.path.dirname(__file__), 'state', 'supervised', 'two_layer', 'random_trained'))
    player_two = HumanPlayer(name='Me')
    while True:
        game.play(players=[player_one, player_two])


def play_human_and_supervised():
    game = Game()
    player_one = SupervisedDeepPlayer(name='Super', version='two_layer')
    player_one.load_state(os.path.join(os.path.dirname(__file__),
                                       'state', 'supervised', 'two_layer', 'random_trained'))
    player_two = HumanPlayer(name='Me')
    player_queue = deque([player_one, player_two])

    # batch = []
    # board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # move = 4
    # for y in range(10000):
    #     batch.append((list(board), move))

    while True:
        game.play(players=player_queue)
        player_queue.rotate()
        # player_one.print_state()
        # for i in range(100):
        #     print(i)
        #     pprint(player_one.player.train_batch(batch))
        #     # print('\n' + '-' * 80 + '\n')
        #     # player_one.print_state()
        # player_one.print_state()


if __name__ == '__main__':
    # play_human_vs_minmax()
    # play_human_player_one()
    # play_human_player_two()
    # play_human_and_first_trained()
    # play_human_and_value_trained()
    # play_value_vs_minmax_manytimes()
    # play_human_and_supervised()
    play_two_layer_vs_human()