"""
This module provides code for working with the tic-tac-toe game, including a few
example players
"""
import itertools
import random


class Board:
    """
    The board for the tic-tac-toe game
    """
    ROWS = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    COLS = [(0, 3, 6), (1, 4, 7), (2, 5, 8)]
    DIAGS = [(0, 4, 8), (2, 4, 6)]

    def __init__(self):
        self.reset()

    @property
    def board(self):
        """
        A property to just return the raw board as a state
        """
        return tuple(self._board)

    def reset(self):
        """
        Reset the board to empty state
        """
        self._board = [0] * 9

    @property
    def available_actions(self):
        """
        Return the list of positions that can be played
        """
        return tuple(i for i in range(len(self._board)) if self._board[i] == 0)

    def apply_action(self, piece, action):
        """
        Apply a move to the board (fail if invalid)
        """
        if self._board[action] != 0:
            raise ValueError(f'Position {place} has already been taken')

        self._board[action] = piece

    @property
    def winner(self):
        """
        Determing if one piece wins or not (piece is -1 and 1)
        """
        for p in (-1, 1):
            win_sum = p*3
            for path in itertools.chain(Board.ROWS, Board.COLS, Board.DIAGS):
                if sum(self._board[i] for i in path) == win_sum:
                    return p

        if len(self.available_actions) == 0:
            return 0

        return None


class Game:
    """
    The actual tic-tac-toe game loop
    """
    def __init__(self, board=None):
        self._board = board or Board()

    def play_game(self, player_one, player_two):
        """
        play_game will start up the new game and trigger the actual gaming loop
        """
        self._board.reset()
        player_one.start(piece=1)
        player_two.start(piece=-1)

        current_player, next_player = player_one, player_two
        current_piece, next_piece = 1, -1

        while self._board.winner is None:
            state = self._board.board
            actions = self._board.available_actions

            selected_action = current_player.make_move(state=state, actions=actions)
            self._board.apply_action(piece=current_piece, action=selected_action)

            current_piece, next_piece = next_piece, current_piece
            current_player, next_player = next_player, current_player

        winner = self._board.winner
        final_board = self._board.board

        if winner == 0:
            player_one_score, player_two_score = 0, 0
        elif winner == 1:
            player_one_score, player_two_score = 1, -1
        elif winner == -1:
            player_one_score, player_two_score = -1, 1
        else:
            raise ValueError(f'The winner cannot be value {winner}')

        player_one.finish(state=final_board, score=player_one_score)
        player_two.finish(state=final_board, score=player_two_score)


class PerfectPlayer:
    def start(self, piece):
        pass

    def make_move(self, state, actions):
        pass

    def finish(self, state, score):
        pass


class RandomPlayer:
    def start(self, piece):
        pass

    def make_move(self, state, actions):
        return random.choice(actions)

    def finish(self, state, score):
        pass


class InteractivePlayer:
    @staticmethod
    def _map_piece_to_char(piece):
        if piece == 1:
            return 'X'
        if piece == -1:
            return 'O'
        return ' '

    @staticmethod
    def _print_board(board):
        for i in range(3):
            print(f'------------')
            print('|', end='')
            for y in range(3):
                print(f' {InteractivePlayer._map_piece_to_char(board[i*3 + y])}', end=' |')
            print()
        print(f'------------')

    def start(self, piece):
        print(f'Welcome to Tic-Tac-Toe, you are player {InteractivePlayer._map_piece_to_char(piece)}')

    def make_move(self, state, actions):
        InteractivePlayer._print_board(state)
        valid_move = None
        while valid_move is None:
            selection = input(f'Its your turn, what is your move available({actions}): ')
            if not selection.isdigit():
                print(f'Invalid option, not a number {selection}')
            elif int(selection) not in actions:
                print(f'Invalid action {selection}')
            else:
                valid_move = int(selection)

        return valid_move

    def finish(self, state, score):
        InteractivePlayer._print_board(state)
        if score == 0:
            print('Well, looks like you were in a draw')
        elif score == 1:
            print('Congrats, you are the winner')
        elif score == -1:
            print('Sorry, better luck next time')
        else:
            print('Um, what just happened?')
