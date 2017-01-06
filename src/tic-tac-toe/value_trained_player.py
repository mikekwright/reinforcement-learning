import random
import json

class ValueTrainedPlayer:
    def __init__(self, step_value=0.1, exploratory_percent=1.0, name='ValueTrained'):
        self.step_value = step_value
        self.state_values = {}
        self.history = []
        self.exploratory_percent = exploratory_percent
        self.loss_value = 0
        self.draw_value = .25
        # self.draw_value = .50
        self.default_value = .50
        self.win_value = 1
        self.name = name
        self.count = 0

    def start_game(self, piece='X', train=False):
        self.piece = piece
        self.train = train
        self.history = []
        self.count += 1
        if self.count % 10000 == 0:
            self.exploratory_percent = self.exploratory_percent * .6
            print("updated exploratory: ", self.exploratory_percent)

    def __random_move(self, board):
        spots = board.open_spots()
        if len(spots) <= 0:
            return -1
        
        selection = random.randint(0, len(spots)-1)
        return spots[selection]

    def __get_value(self, board):
        key = self.__get_state_key(board, self.piece) 
        return self.__get_state_value(key, board, self.piece)

    def __get_state_key(self, board, piece):
        # return piece + '-' + board.board_state()
        return board.board_state()

    def __best_move(self, board):
        possible_moves = board.open_spots()
        best_move = -1
        best_value = -1000
        for move in possible_moves:
            board_with_move = board.clone_move(move=move, piece=self.piece)
            move_value = self.__get_value(board)
            if move_value > best_value:
                best_value = move_value
                best_move = move
        return best_move


    def make_move(self, board):
        if random.random() < self.exploratory_percent:
            selected_move = self.__random_move(board)
        else:
            selected_move = self.__best_move(board)

        cloned_board = board.clone_move(move=selected_move, piece=self.piece)
        self.history.append(self.__get_state_key(cloned_board, self.piece))
        return selected_move

    def game_over(self, final_board):
        final_state_key = self.__get_state_key(final_board, self.piece)
        final_value = self.__get_state_value(final_state_key, final_board, self.piece)

        primed_value = final_value
        self.history.reverse()
        for history_key in self.history:
            current_value = self.__get_state_value(history_key, final_board, self.piece)
            updated_value = current_value + self.step_value*(primed_value - current_value)
            self.state_values[history_key] = updated_value
            primed_value = updated_value
        # print(self.state_values)

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
