import random

class RandomPlayer:
    def __init__(self):
        self.name = 'Random'

    def start_game(self, piece='X', train=False):
        self.piece = piece

    def make_move(self, board):
        spots = board.open_spots()
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
