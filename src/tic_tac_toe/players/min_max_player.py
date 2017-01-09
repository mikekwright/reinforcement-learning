from logging import debug, info
import random


class MinMaxPlayer:
    def __init__(self, name='MinMax', step_value=0.2, make_imperfect=False, random_percent=0.25):
        info('Creating MinMax player named {}'.format(name))
        self.name = name
        self.player_num = None
        self.step_value = step_value
        self.imperfect = make_imperfect
        self.random_percent = random_percent

    def start_game(self, player_num=0):
        debug('Starting game with RandomPlayer {} as number {}'.format(self.name, player_num))
        self.player_num = player_num

    def make_move(self, board):
        if self.imperfect and random.random() < self.random_percent:
            return board.random_move()
        else:
            move, value = self.__min_max(board, use_max=True)
            debug('Move {} with value {}'.format(move, value))
            return move

    def __min_max(self, board, use_max=True):
        moves = board.moves()
        if board.game_over():
            return -1, board.value(turn=self.player_num)

        # Optimization for the first move
        if len(moves) >= 7:
            debug('Start of gaming using random selection optimization')
            optimized = [0, 2, 4, 6, 8]
            while True:
                selected = random.randint(0, len(optimized) - 1)
                move = optimized[selected]
                if move in moves:
                    return move, board.value(turn=self.player_num)

        selected_move = None
        selected_value = None
        for move in moves:
            debug('looking at move {} - state; {}'.format(move, board.state()))
            cloned = board.clone()
            cloned.apply_move(move)
            (_, new_value) = self.__min_max(board=cloned, use_max=not use_max)

            if selected_move is None:
                selected_move = move
                selected_value = new_value

            if use_max:
                if new_value > selected_value:
                    selected_value = new_value
                    selected_move = move
            else:
                if new_value < selected_value:
                    selected_value = new_value
                    selected_move = move

        debug('selected_move {} - selected_value {} - state {}'.format(selected_move, selected_value, board.state()))
        return selected_move, selected_value

    def game_over(self, final_board):
        debug('Game over for MinMax {}'.format(self.name))

    def store_state(self, filename):
        debug('Request to store state for MinMax {}'.format(self.name))

    def load_state(self, filename):
        debug('Request to load state for MinMax {}'.format(self.name))

    def print_state(self):
        print('No state for MinMax')

    def enable_training(self):
        debug('Request to enable training for MinMax {}'.format(self.name))

    def disable_training(self):
        debug('Request to disable training for MinMax {}'.format(self.name))
