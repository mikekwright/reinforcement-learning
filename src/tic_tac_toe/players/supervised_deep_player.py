from logging import debug, info
from colorama import init, Fore, Back, Style
init()

from .min_max_player import MinMaxPlayer
from .deep import OneLayerPlayer, TwoLayerPlayer, ThreeLayerPlayer


class SupervisedDeepPlayer:
    def __init__(self, name=None,
                 training_player=MinMaxPlayer(name='Supervised-MinMax', make_imperfect=False),
                 version='one_layer',
                 log_verbose=False,
                 train_size=1,
                 params=None):

        if params is None:
            params = {}
        if name is not None:
            params['name'] = name
        params['log_verbose'] = log_verbose
        if version == 'one_layer':
            self.player = OneLayerPlayer(**params)
        elif version == 'two_layer':
            self.player = TwoLayerPlayer(**params)
        elif version == 'three_layer':
            self.player = ThreeLayerPlayer(**params)
        else:
            raise ValueError('Unknown deep version {} used'.format(version))
        self.name = self.player.name
        self.training = False
        self.training_player = training_player
        self.train_size = train_size
        self.training_batch = []

    def start_game(self, player_num=0):
        debug('Starting game with SupervisedDeepPlayer {}'.format(player_num))
        # self.training_batch = []
        self.player.start_game(player_num=player_num)
        if self.training:
            self.training_player.start_game(player_num=player_num)

    def make_move(self, board):
        move = self.player.make_move(board)
        if self.training:
            target_move = self.training_player.make_move(board)
            training_entry = (list(board.board), target_move)
            if self.train_size == 1:
                self.player.train_batch([training_entry])
            else:
                self.training_batch.append(training_entry)
        return move

    def __run_training(self):
        info(Fore.LIGHTYELLOW_EX +
             'Running batch training of size {}'.format(len(self.training_batch)) +
             Style.RESET_ALL)
        self.player.train_batch(self.training_batch)
        self.training_batch = []

    def game_over(self, final_board):
        debug('SupervisedDeepPlayer game over with board state: {}'.format(final_board.state()))
        self.player.game_over(final_board=final_board)
        self.training_player.game_over(final_board=final_board)
        if self.training and len(self.training_batch) > self.train_size:
            self.__run_training()

    def store_state(self, filename):
        self.player.store_state(filename=filename)

    def load_state(self, filename):
        self.player.load_state(filename=filename)

    def print_state(self):
        self.player.print_state()

    def enable_training(self):
        debug('Request to enable training for SupervisedDeepPlayer')
        self.training = True
        self.training_batch = []

    def disable_training(self):
        debug('Request to disable training for SupervisedDeepPlayer')
        if len(self.training_batch) > 0:
            self.__run_training()
        self.training = False

    def can_train(self):
        return True
