import random
from logging import debug, info
from colorama import init, Fore, Style
init()


class Board:
    def __init__(self, board=None, turn=1, player_one='X', player_two='O'):
        if board is None:
            self.board = [0, 0, 0,
                          0, 0, 0,
                          0, 0, 0]
        else:
            self.board = board
        self.turn = turn
        self.player_one = player_one
        self.player_two = player_two
        self.win_value = 1
        self.loss_value = 0
        self.draw_value = 0.5
        self.default_value = 0.5

    def clone(self):
        return Board(board=list(self.board), turn=self.turn)

    def moves(self):
        return [index for index, option in enumerate(self.board) if option == 0]

    def state(self, turn=None):
        turn = self.turn if turn is None else turn
        return str(turn) + '-' + ''.join([str(l) for l in self.board])

    def random_move(self):
        spots = self.moves()
        if len(spots) <= 0:
            return -1

        selection = random.randint(0, len(spots)-1)
        return spots[selection]

    def value(self, turn=0):
        turn = turn if turn != 0 else self.turn

        if turn == 1:
            opponent = 2
        else:
            opponent = 1

        if self.does_player_win(player=turn):
            return self.win_value
        elif self.does_player_win(player=opponent):
            return self.loss_value
        elif self.is_draw():
            return self.draw_value
        else:
            return self.default_value

    def apply_move(self, move):
        debug('Applying move {}'.format(move))
        if self.board[move] == 0:
            self.board[move] = self.turn
        else:
            raise ValueError("move already been taken")

        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

    def game_over(self):
        if self.does_player_win(player=1) or self.does_player_win(player=2) or self.is_draw():
            return True

        return False

    def is_draw(self):
        if len(self.moves()) == 0 and not self.does_player_win(player=1) and not self.does_player_win(player=2):
            return True

        return False

    def does_player_win(self, player=1):
        if self.__check_for_row_win(player):
            return True
        
        if self.__check_for_column_win(player):
            return True

        if self.__check_for_diagonal_win(player):
            return True

        return False

    def print_board(self):
        print(Fore.LIGHTBLUE_EX, end='')
        for row in range(3):
            offset = row*3
            print(self.__player_symbol(self.board[offset]), '|',
                  self.__player_symbol(self.board[offset+1]), '|',
                  self.__player_symbol(self.board[offset+2]))
            if row < 2:
                print("-" * 9)
        print(Style.RESET_ALL, end='')

    def __player_symbol(self, board_value):
        if board_value == 0:
            return ' '
        elif board_value == 1:
            return self.player_one
        else:
            return self.player_two

    def __check_for_column_win(self, player):
        for column in range(3):
            top = column
            middle = column+3
            bottom = column+6

            if self.board[top] == self.board[middle] == self.board[bottom] == player:
                return True
        return False

    def __check_for_row_win(self, player):
        for row in range(3):
            left = (row*3)
            middle = (row*3) + 1
            right = (row*3) + 2

            if self.board[left] == self.board[middle] == self.board[right] == player:
                return True

        return False

    def __check_for_diagonal_win(self, player):
        top_left = 0
        top_right = 2
        middle = 4
        bottom_left = 6
        bottom_right = 8

        if self.board[top_left] == self.board[middle] == self.board[bottom_right] == player:
            return True
        
        if self.board[top_right] == self.board[middle] == self.board[bottom_left] == player:
            return True
        
        return False

