#!/usr/bin/env python3

import time

from board import Board
from random_player import RandomPlayer
from trained_player import TrainedPlayer


class Game:
    def __init__(self):
        pass

    def train(self, count=100, player_one=RandomPlayer(), player_two=TrainedPlayer()):
        first = player_one
        second = player_two
        for i in range(count+1):
            if i == 1 or i % 100 == 0 and not i == 0:
                print("Running train #", i)

            self.__play_game(print_board=False, o=first, x=second, train=True)

            tmp = first 
            first = second 
            second = tmp

        return (player_one, player_two)

    def play(self, player_one=RandomPlayer(), player_two=RandomPlayer(), trace=True):
        board = self.__play_game(print_board=trace, o=player_one, x=player_two)

        if board.is_draw():
            print('Game Over - Draw')
        elif board.does_piece_win('X'):
            print('Game Over, X Wins (', player_two.name, ')')
        elif board.does_piece_win('O'):
            print('Game Over, O Wins (', player_one.name, ')')

    def print_debug(self):
        self.player_two.print_states()


    def __play_game(self, o, x, print_board=False, train=False):
        o.start_game(piece='O', train=train)
        x.start_game(piece='X', train=train)

        board = Board()

        turn = 'O'
        while not board.game_over():
            if turn == 'O':
                move = o.make_move(board)
                board.apply_move(move=move, piece='O')
                turn = 'X'
            else:
                move = x.make_move(board)
                board.apply_move(move=move, piece='X')
                turn = 'O'

            if print_board:
                board.print_board()
                print()
                time.sleep(0.25)

        o.game_over(board)
        x.game_over(board)

        return board


if __name__ == "__main__": 
    game = Game()
    _, trained_one = game.train(count=10000, player_two=TrainedPlayer(name='one'))
    _, trained_two = game.train(count=100000, player_one=trained_one, player_two=TrainedPlayer(name='two'))
    game.play(player_one=trained_one)
    for i in range(50):
        game.play(player_one=trained_one, player_two=trained_two, trace=False)


