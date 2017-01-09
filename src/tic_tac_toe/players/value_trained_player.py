import random
import json
from pprint import pprint

class ValueTrainedPlayer:
    def __init__(self, step_value=0.2, exploratory_percent=0.15, name='ValueTrained'):
        self.step_value = step_value
        self.state_values = {}
        self.exploratory_percent = exploratory_percent
        self.loss_value = 0
        # self.draw_value = .25
        self.draw_value = .50
        self.default_value = .50
        self.win_value = 1
        self.name = name
        self.count = 0
        self.debug_enabled = False

    def start_game(self, piece='X', train=False):
        self.piece = piece
        self.train = train
        self.last_move_state = None
        self.count += 1
        if self.count % 100000 == 0:
            self.exploratory_percent = self.exploratory_percent * .6
            # self.step_value = self.step_value * .8

    def __random_move(self, board):
        spots = board.open_spots()
        if len(spots) <= 0:
            return -1
        selection = random.randint(0, len(spots)-1)
        return spots[selection]

    def __get_value(self, board):
        key = self.__get_state_key(board, self.piece)
        # print("Get value: ", key)
        return self.__get_state_value(key, board, self.piece)

    def __get_state_key(self, board, piece):
        # return piece + '-' + board.board_state()
        return board.board_state()

    def __best_move(self, board):
        possible_moves = board.open_spots()
        if self.debug_enabled:
            print("Selecting best move", possible_moves)
        # print(possible_moves)
        best_move = -1
        best_value = -1000
        for move in possible_moves:
            board_with_move = board.clone_move(move=move, piece=self.piece)
            move_value = self.__get_value(board_with_move)
            if move_value > best_value:
                best_value = move_value
                best_move = move
            if self.debug_enabled:
                print(board_with_move.board_state(),move_value)
            # print(self.state_values)
        return best_move

    def __update_move_value(self, board):
        # print("Updating value ", self.last_move_state)
        if self.last_move_state != None:
            key, exploratory = self.last_move_state
            last_move_value = self.state_values.get(key, self.default_value)
            if exploratory:
                return

            board_value = self.__get_value(board)
            updated_move_value = last_move_value + self.step_value*(board_value - last_move_value)
            # print("key: ", key, "from ", last_move_value, "to ", updated_move_value)
            self.state_values[key] = updated_move_value

    def make_move(self, board):
        self.__update_move_value(board)
        if random.random() < self.exploratory_percent:
            selected_move = self.__random_move(board)
            exploratory = True
        else:
            selected_move = self.__best_move(board)
            exploratory = False

        # Add our move
        cloned_board = board.clone_move(move=selected_move, piece=self.piece)
        self.last_move_state = (self.__get_state_key(cloned_board, self.piece), exploratory)

        return selected_move

    def debug(self, enabled):
        self.debug_enabled = enabled

    def game_over(self, final_board):
        self.__update_move_value(final_board)
        # print("Over: ", self.history)
        # final_state_key = self.__get_state_key(final_board, self.piece)
        # final_value = self.__get_state_value(final_state_key, final_board, self.piece)

        # primed_value = final_value
        # self.history.reverse()
        # # print("Reverse: ", self.history)
        # for history_key in self.history:
            # if history_key not in self.state_values:
                # current_value = self.default_value
            # else:
                # current_value = self.state_values[history_key]
            # updated_value = current_value + self.step_value*(primed_value - current_value)
            # self.state_values[history_key] = updated_value
            # primed_value = updated_value
        # pprint(self.state_values)

    def __get_state_value(self, key, board, piece):
        if key not in self.state_values:
            if board.is_draw():
                self.state_values[key] = self.draw_value
            elif board.does_piece_win(piece):
                self.state_values[key] = self.win_value
            elif board.does_piece_win(board.opposite_piece(piece)):
                self.state_values[key] = self.loss_value
            else:
                self.state_values[key] = self.default_value
        return self.state_values[key]

    def store_state(self, filename):
        with open(filename, 'w') as fp:
            json.dump(self.state_values, fp, sort_keys=True, indent=4)

    def load_state(self, filename):
        pass

    def print_state(self):
        print(self.state_values)
