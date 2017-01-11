import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))

from tic_tac_toe.game import Game
from tic_tac_toe.players import RandomPlayer, MinMaxPlayer


class GenerateGames:
    def __init__(self, game_count=10000):
        self.game_count = game_count
        self.game = Game()

    def run_games(self, player_one, player_two, keep=1):
        plays = []
        draw, win, loss = 0, 0, 0
        players = [player_one, player_two]
        for i in range(self.game_count):
            result, history = self.game.play(players=players)
            if keep == 1:
                filtered = [x for idx, x in enumerate(history) if idx % 2 == 0]
            else:
                filtered = [x for idx, x in enumerate(history) if idx % 2 == 1]
            plays.append(filtered)

            if result == 0:
                draw += 1
            elif result == keep:
                win += 1
            else:
                print(history)
                loss += 1

        print('Completed training - draw: {} - win: {} - loss: {}'.format(draw, win, loss))
        return plays

    def create_game_history(self, player_one_filename, player_two_filename):
        player_one = MinMaxPlayer()
        player_two = RandomPlayer()
        one_history = self.run_games(player_one, player_two, keep=1)
        with open(player_one_filename, 'w') as one_fp:
            # json.dump(one_history, fp=one_fp, sort_keys=False, indent=4)
            for game in one_history:
                one_fp.write(str(game) + '\n')

        two_history = self.run_games(player_two, player_one, keep=2)
        with open(player_two_filename, 'w') as two_fp:
            json.dump(two_history, fp=two_fp, sort_keys=False, indent=4)


if __name__ == "__main__":
    generator = GenerateGames()
    player_one_history = os.path.join(os.path.dirname(__file__), 'state', 'history', 'player_one.json')
    player_two_history = os.path.join(os.path.dirname(__file__), 'state', 'history', 'player_two.json')
    generator.create_game_history(player_one_filename=player_one_history, player_two_filename=player_two_history)
