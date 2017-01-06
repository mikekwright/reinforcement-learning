class Board:
    def __init__(self):
        self.board = [' ', ' ', ' ',
                      ' ', ' ', ' ',
                      ' ', ' ', ' ']

    def clone_move(self, piece, move):
        clone_board = Board()
        clone_board.board = list(self.board)
        clone_board.apply_move(move=move, piece=piece)
        return clone_board

    def open_spots(self):
        return [index for index, option in enumerate(self.board) if option == ' ']

    def board_state(self):
        return ''.join(self.board)

    def opposite_piece(self, piece):
        return 'X' if piece == 'O' else 'O'

    def apply_move(self, move, piece):
        if self.board[move] == ' ':
            self.board[move] = piece
        else:
            raise ValueError("move already been taken")

    def game_over(self):
        if self.does_piece_win(piece='X') or self.does_piece_win(piece='O') or self.is_draw():
            return True

        return False

    def is_draw(self):
        if len(self.open_spots()) == 0 and not self.does_piece_win(piece='X') and not self.does_piece_win(piece='O'):
            return True

        return False

    def does_piece_win(self, piece='O'):
        if self.__check_for_row_win(piece):
            return True
        
        if self.__check_for_column_win(piece):
            return True

        if self.__check_for_diagonal_win(piece):
            return True

        return False

    def print_board(self):
        for row in range(3):
            offset = row*3;
            print(self.board[offset], '|', self.board[offset+1], '|', self.board[offset+2])
            if row < 2:
                print("-" * 9)

    def __check_for_column_win(self, piece):
        for column in range(3):
            top = column
            middle = column+3
            bottom = column+6

            if self.board[top] == self.board[middle] == self.board[bottom] == piece:
                return True
        return False


    def __check_for_row_win(self, piece):
        for row in range(3):
            left = (row*3)
            middle = (row*3) + 1
            right = (row*3) + 2

            if self.board[left] == self.board[middle] == self.board[right] == piece:
                return True

        return False

    def __check_for_diagonal_win(self, piece):
        top_left = 0
        top_right = 2
        middle = 4
        bottom_left = 6
        bottom_right = 8

        if self.board[top_left] == self.board[middle] == self.board[bottom_right] == piece:
            return True
        
        if self.board[top_right] == self.board[middle] == self.board[bottom_left] == piece:
            return True
        
        return False

