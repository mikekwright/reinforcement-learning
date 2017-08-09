from tic_tac_toe import Game, RandomPlayer, PerfectPlayer, InteractivePlayer


def play_game(count=1):
    player_one = RandomPlayer()
    player_two = InteractivePlayer()

    game = Game()

    game.play_game(player_one, player_two)


if __name__ == "__main__":
    play_game()
