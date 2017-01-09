import random
import json
from pprint import pprint
from logging import debug, info, error


class ValueTrainedPlayer:
    def __init__(self, step_value=0.2, exploratory_percent=0.15, convergence_rate=10000, name='ValueTrained'):
        self.step_value = step_value
        self.state_values = {}
        self.exploratory_percent = exploratory_percent
        self.loss_value = 0
        self.draw_value = .50
        self.default_value = .50
        self.win_value = 1
        self.name = name
        self.count = 0
        self.convergence_rate = convergence_rate
        self.training = False

    def start_game(self, player_num=1):
        self.player_num = player_num
        self.last_move_state = None
        self.count += 1
        if self.count % self.convergence_rate == 0:
            self.exploratory_percent *= .6
            self.step_value *= .8

    def __best_move(self, board):
        possible_moves = board.moves()
        debug('Selecting best move from {}'.format(str(possible_moves)))

        best_move = None
        best_value = None
        for move in possible_moves:
            board_with_move = board.clone()
            board_with_move.apply_move(move)
            move_value = self.__get_value_of_board(board_with_move)
            if best_move is None or move_value > best_value:
                best_value = move_value
                best_move = move

            debug('move {} value {} new_best_move {}'.format(move, move_value, best_move))
        return best_move

    def make_move(self, board):
        if random.random() < self.exploratory_percent:
            selected_move = board.random_move()
            exploratory = True
        else:
            selected_move = self.__best_move(board)
            exploratory = False

        move_board = board.clone()
        move_board.apply_move(selected_move)
        key = move_board.state(turn=self.player_num)
        if not key in self.state_values:
            self.state_values[key] = move_board.value()

        if not exploratory and self.last_move_state is not None:
            self.__update_last_move_value(move_board)

        self.last_move_state = move_board.state(turn=self.player_num)
        return selected_move

    def __update_last_move_value(self, selected_move_board):
        if not self.training:
            return

        original_value = self.__get_value_of_key(self.last_move_state)
        move_value = self.__get_value_of_board(selected_move_board)
        adjusted_value = original_value + self.step_value * (move_value - original_value)
        self.state_values[self.last_move_state] = adjusted_value

    def game_over(self, final_board):
        if self.last_move_state is None:
            error('Game is over and last move state does not exist')
        self.__update_last_move_value(final_board)

    def __get_value_of_board(self, board):
        key = board.state(turn=self.player_num)
        if key not in self.state_values:
            self.state_values[key] = board.value(turn=self.player_num)
        return self.__get_value_of_key(key)

    def __get_value_of_key(self, key):
        return self.state_values[key]

    def store_state(self, filename):
        info('Saving state for ValueTrainedPlayer {} - file {}'.format(self.name, filename))
        with open(filename, 'w') as fp:
            json.dump(self.state_values, fp, sort_keys=True, indent=4)

    def load_state(self, filename):
        info('Loading state for ValueTrainedPlayer {} - file {}'.format(self.name, filename))
        with open(filename, 'r') as fp:
            self.state_values = json.load(fp)

    def print_state(self):
        pprint(self.state_values)

    def enable_training(self):
        debug('Enabled training for ValueTrainedPlayer {}'.format(self.name))
        self.training = True

    def disable_training(self):
        debug('Disabled training for ValueTrainedPlayer {}'.format(self.name))
        self.training = False

    def can_train(self):
        return True