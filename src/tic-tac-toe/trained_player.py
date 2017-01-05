import random

class TrainedPlayer:
    def __init__(self, step_value=0.1, exploratory_percent=0.1, name='Trained'):
        self.step_value = step_value
        self.state_values = {}
        self.exploratory_percent = exploratory_percent
        self.loss_value = 0
        self.draw_value = .25
        self.default_value = .50
        self.win_value = 1
        self.name = name

    def start_game(self, piece='X', train=False):
        self.piece = piece
        self.move_history = []
        self.train = train

    def make_move(self, board):
        if self.train and random.random() < self.exploratory_percent:
            move = self.__make_random_move(board)
        else:
            move = self.__select_best_move(board)
        self.move_history.append((board.board_state(), move))
        return move

    def __select_best_move(self, board):
        board_state = board.board_state()
        open_spots = board.open_spots()
        if board_state not in self.state_values:
            self.state_values[board_state] = {} 

        state_values = self.state_values[board_state]
        for spot in open_spots:
            if spot not in state_values:
                state_values[spot] = self.default_value

        best_move_value = self.loss_value
        choosen_move = -1
        for move in state_values:
            if state_values[move] >= best_move_value:
                choosen_move = move
                best_move_value = state_values[move]
                

        return choosen_move

        
    def __make_random_move(self, board):
        spots = board.open_spots()
        if len(spots) <= 0:
            return -1
        
        selection = random.randint(0, len(spots)-1)
        return spots[selection]


    def game_over(self, final_board):
        if not self.train:
            return

        adjust_value = self.default_value
        if final_board.does_piece_win(piece=self.piece):
            adjust_value = self.win_value
        elif final_board.is_draw():
            adjust_value = self.draw_value
        else:
            adjust_value = self.loss_value
        self.__adjust_state_values(value_prime=adjust_value)

    def print_state(self):
        print(self.state_values)

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
        pass

    def load_state(self, filename):
        pass

