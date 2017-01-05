class HumanPlayer:
    def __init__(self):
        self.name = 'Human'

    def start_game(self, piece='X', train=False):
        self.piece = piece

    def make_move(self, board):
        # board.print_board()
        option = input("You are %s, what is your move (0 top left): " % self.piece)
        return int(option)
        
    def game_over(self, final_board):
        pass

    def store_state(self, filename):
        pass

    def load_state(self, filename):
        pass

    def print_state(self):
        print('No state for Random')
