from logging import debug, info

from .board import Board


class Game:
    def __init__(self):
        pass

    def play(self, players): # player_one, player_two):
        if len(players) != 2:
            raise ValueError('Cannot play tic tac toe without exactly 2 players')

        player_one, player_two = players
        (board, history) = self.__play_game(player_one=player_one, player_two=player_two)

        if board.is_draw():
            debug('Game Over - Draw')
            return 0, history
        elif board.does_player_win(player=1):
            debug('Game Over, X Wins ({})'.format(player_two.name))
            return 1, history
        elif board.does_player_win(player=2):
            debug('Game Over, O Wins ({})'.format(player_one.name))
            return 2, history
        else:
            return -1, history

    def __play_game(self, player_one, player_two):
        player_one.start_game(player_num=1)
        player_two.start_game(player_num=2)

        board = Board()
        history = []

        turn = player_one
        while not board.game_over():
            move = turn.make_move(board=board)
            history.append((list(board.board), move))
            board.apply_move(move=move)
            turn = player_two if turn == player_one else player_one

        player_one.game_over(board)
        player_two.game_over(board)

        return board, history
