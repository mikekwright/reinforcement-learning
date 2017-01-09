from logging import debug, info

from .board import Board


class Game:
    def __init__(self):
        pass

    def play(self, players): # player_one, player_two):
        if len(players) != 2:
            raise ValueError('Cannot play tic tac toe without exactly 2 players')

        player_one, player_two = players
        board = self.__play_game(player_one=player_one, player_two=player_two)

        if board.is_draw():
            debug('Game Over - Draw')
        elif board.does_player_win(player=1):
            debug('Game Over, X Wins ({})'.format(player_two.name))
        elif board.does_player_win(player=2):
            debug('Game Over, O Wins ({})'.format(player_one.name))

    def __play_game(self, player_one, player_two):
        player_one.start_game(player_num=1)
        player_two.start_game(player_num=2)

        board = Board()

        turn = player_one
        while not board.game_over():
            move = turn.make_move(board=board)
            board.apply_move(move=move)
            turn = player_two if turn == player_one else player_one

        player_one.game_over(board)
        player_two.game_over(board)

        return board

#
# if __name__ == "__main__":
#     game = Game()
    # _, trained_one = game.train(count=10000, player_one=HumanPlayer(), player_two=ValueTrainedPlayer(name='one'))
    # _, trained_one = game.train(count=1000000, player_two=ValueTrainedPlayer(name='one'))
    # _, trained_one = game.train(count=100000, player_two=ValueTrainedPlayer(name='one'))
    # _, trained_one = game.train(count=100000, player_two=FirstTrainedPlayer(name='one'))
    # _, trained_two = game.train(count=10000, player_one=trained_one, player_two=FirstTrainedPlayer(name='two'))
    # _, trained_two = game.train(count=10000, player_one=trained_one, player_two=ValueTrainedPlayer(name='two'))
    # trained_one, trained_two = game.train(count=10000000,
    #                                       player_one=ValueTrainedPlayer(name='one'),
    #                                       player_two=FirstTrainedPlayer(name='two'))
    #
    # print("\nTraining complete, AI vs Random")
    # game.play(player_one=trained_one)
    #
    # print("\nAI vs Human")
    # trained_one.debug(enabled=True)
    # game.play(player_one=trained_one, player_two=HumanPlayer())
    # trained_one.debug(enabled=False)
    #
    # print("\nAI vs AI, 50 times")
    # for i in range(50):
    #     game.play(player_one=trained_one, player_two=trained_two, trace=False)
    #
    # trained_one.store_state('./state/trained_one_latest.json')
    # trained_two.store_state('./state/trained_two_latest.json')

