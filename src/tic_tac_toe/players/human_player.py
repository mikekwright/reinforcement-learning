from logging import debug, info
from colorama import init, Fore, Style
init()


class HumanPlayer:
    def __init__(self, name='Human'):
        info('Creating human player named {}'.format(name))
        self.name = name
        self.player_num = None

    def start_game(self, player_num=0):
        debug('Starting game with player {} as number {}'.format(self.name, player_num))
        self.player_num = player_num

    def make_move(self, board):
        board.print_board()
        possible_moves = board.moves()
        while True:
            option = input('What is your move (0 top left) {}: '.format(possible_moves))
            result = int(option) if option.isdigit() else None
            if result in possible_moves:
                break
            else:
                print('Invalid choice {}'.format(result))
        print()
        return result

    def game_over(self, final_board):
        debug('Game over with HumanPlayer {}'.format(self.name))
        if final_board.is_draw():
            print(Fore.RED + 'The game is a draw' + Style.RESET_ALL)
        elif final_board.does_player_win(self.player_num):
            print(Fore.GREEN + 'Player {} has won!'.format(self.name) + Style.RESET_ALL)
        else:
            print(Fore.RED + 'Player {} has lost'.format(self.name) + Style.RESET_ALL)
        final_board.print_board()
        print()

    def store_state(self, filename):
        info('Request to save state for HumanPlayer {} - filename {}'.format(self.name, filename))

    def load_state(self, filename):
        info('Request to load state for HumanPlayer {} - filename {}'.format(self.name, filename))

    def print_state(self):
        debug('Request to print state for HumanPlayer {}'.format(self.name))

    def enable_training(self):
        debug('Request to enable training for HumanPlayer {}'.format(self.name))

    def disable_training(self):
        debug('Request to disable training for HumanPlayer {}'.format(self.name))

    def can_train(self):
        return False
