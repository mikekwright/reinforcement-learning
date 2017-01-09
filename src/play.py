import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from tic_tac_toe import Game
from tic_tac_toe.players import HumanPlayer, RandomPlayer


if __name__ == '__main__':
    game = Game()
    player_one = HumanPlayer()
    player_two = RandomPlayer()
    game.play(players=[player_one, player_two])
