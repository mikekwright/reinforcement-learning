from logging import debug, info, warn
from pprint import pprint

import random
import json


class FirstTrainedPlayer:
    def __init__(self, step_value=0.1, exploratory_percent=0.3, name='FirstTrained'):
        self.step_value = step_value
        self.exploratory_percent = exploratory_percent
        self.name = name
        self.__setup_defaults()

    def __setup_defaults(self):
        self.state_values = {}
        self.loss_value = 0
        self.draw_value = .25
        self.default_value = .50
        self.win_value = 1
        self.player_num = None
        self.training = False

    def start_game(self, player_num=0):
        debug('Starting game with player {} as number {}'.format(self.name, player_num))
        self.player_num = player_num
        self.move_history = []

    def make_move(self, board):
        if self.training and random.random() < self.exploratory_percent:
            move = board.random_move()
        else:
            move = self.__select_best_move(board)
        self.move_history.append((board.state(), move))
        debug('Selected move {} for FirstTrained {}'.format(move, self.name))
        return move

    def __select_best_move(self, board):
        board_state = board.state()
        open_spots = board.moves()
        if board_state not in self.state_values:
            self.state_values[board_state] = {} 

        state_values = self.state_values[board_state]
        for spot in open_spots:
            if spot not in state_values:
                state_values[spot] = self.default_value

        best_move_value = self.loss_value
        chosen_move = -1
        for move in state_values:
            if state_values[move] >= best_move_value:
                chosen_move = move
                best_move_value = state_values[move]
                
        return int(chosen_move)

    def game_over(self, final_board):
        if not self.training:
            return

        if final_board.does_player_win(player=self.player_num):
            adjust_value = self.win_value
        elif final_board.is_draw():
            adjust_value = self.draw_value
        else:
            adjust_value = self.loss_value
        self.__adjust_state_values(value_prime=adjust_value)

    def __adjust_state_values(self, value_prime):
        while len(self.move_history) > 0:
            last_state,last_move = self.move_history.pop()
            if not last_state in self.state_values:
                self.state_values[last_state] = {}
            if not last_move in self.state_values[last_state]: 
                self.state_values[last_state] = {last_move: self.default_value}

            move_value = self.state_values[last_state][last_move] 
            adjusted_value = move_value + self.step_value*(value_prime-move_value)
            self.state_values[last_state][last_move] = adjusted_value
            value_prime = adjusted_value

    def store_state(self, filename):
        info('Saving state for FirstTrainedPlayer {} - file {}'.format(self.name, filename))
        with open(filename, 'w') as fp:
            json.dump(self.state_values, fp, sort_keys=True, indent=4)

    def load_state(self, filename):
        info('Loading state for FirstTrainedPlayer {} - file {}'.format(self.name, filename))
        with open(filename, 'r') as fp:
            self.state_values = json.load(fp)

    def enable_training(self):
        debug('Enabled training for FirstTrainedPlayer {}'.format(self.name))
        self.training = True

    def disable_training(self):
        debug('Disabled training for FirstTrainedPlayer {}'.format(self.name))
        self.training = False

    def print_state(self):
        pprint(self.state_values)

    def can_train(self):
        return True
