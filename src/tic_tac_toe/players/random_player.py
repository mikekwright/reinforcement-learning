from logging import debug, info

import random


class RandomPlayer:
    def __init__(self, name='Random'):
        info('Creating random player named {}'.format(name))
        self.name = name
        self.player_num = None

    def start_game(self, player_num=0):
        debug('Starting game with RandomPlayer {} as number {}'.format(self.name, player_num))
        self.player_num = player_num

    def make_move(self, board):
        spots = board.moves()
        if len(spots) <= 0:
            return -1
        
        selection = random.randint(0, len(spots)-1)
        return spots[selection]

    def game_over(self, final_board):
        pass

    def store_state(self, filename):
        pass

    def load_state(self, filename):
        pass

    def print_state(self):
        print('No state for Random')

    def enable_training(self):
        debug('Request to enable training for HumanPlayer {}'.format(self.name))

    def disable_training(self):
        debug('Request to disable training for HumanPlayer {}'.format(self.name))
