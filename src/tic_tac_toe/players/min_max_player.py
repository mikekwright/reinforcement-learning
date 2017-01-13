from logging import debug, info
import random


class MinMaxPlayer:
    def __init__(self, name='MinMax', step_value=0.2, make_imperfect=False, random_percent=0.25, cache=True):
        info('Creating MinMax player named {}'.format(name))
        self.name = name
        self.player_num = None
        self.step_value = step_value
        self.imperfect = make_imperfect
        self.random_percent = random_percent
        self.state_cache = {}
        self.cache = cache

    def clear_cache(self):
        self.state_cache = {}

    def start_game(self, player_num=0):
        debug('Starting game with RandomPlayer {} as number {}'.format(self.name, player_num))
        self.player_num = player_num

    def make_move(self, board):
        if self.imperfect and random.random() < self.random_percent:
            return board.random_move()
        else:
            move, value, level = self.__min_max(board, use_max=True)
            debug('Move {} with value {}'.format(move, value))
            return move

    def __min_max(self, board, use_max=True):
        board_state = board.state()
        if self.cache and board_state in self.state_cache:
            return self.state_cache[board_state]

        moves = board.moves()
        if board.game_over():
            result = (-1, board.value(turn=self.player_num), 0)
            if self.cache:
                self.state_cache[board_state] = result
            return result

        # Optimization for the first move
        if len(moves) >= 8:
            debug('Start of gaming using random selection optimization')
            center = 4
            if center in moves:
                return (center, board.value(), 0)
            corners = [0, 2, 6, 8]
            while True:
                selected = random.randint(0, len(corners) - 1)
                move = corners[selected]
                if move in moves:
                    result = (move, board.value(turn=self.player_num), 0)
                    if self.cache:
                        self.state_cache[board_state] = result
                    #return move, board.value(turn=self.player_num)
                    return result

        selected_move = None
        selected_value = None
        selected_move_level = 0
        for move in moves:
            cloned = board.clone()
            cloned.apply_move(move)
            (_, new_value, move_level) = self.__min_max(board=cloned, use_max=not use_max)
            debug('looking at move {} - state; {} - depth {}'.format(move, board.state(), move_level))

            if selected_move is None:
                selected_move = move
                selected_value = new_value
                selected_move_level = move_level
                continue

            if use_max:
                if (new_value == selected_value and move_level < selected_move_level) or (new_value > selected_value):
                    selected_value = new_value
                    selected_move = move
                    selected_move_level = move_level
            else:
                if (new_value == selected_value and move_level < selected_move_level) or (new_value < selected_value):
                    selected_value = new_value
                    selected_move = move
                    selected_move_level = move_level

        debug('selected_move {} - selected_value {} - state {}'.format(selected_move, selected_value, board.state()))
        result = (selected_move, selected_value, selected_move_level+1)
        if self.cache:
            self.state_cache[board_state] = result
        return result

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

    def can_train(self):
        return False
