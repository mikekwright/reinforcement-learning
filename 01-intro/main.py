import click

from tic_tac_toe import Game, RandomPlayer, InteractivePlayer
from ai_player import AIPlayer


@click.group()
def app():
    """
    This is basically a wrapper for groups of cli commands
    """
    pass


@app.command()
@click.argument('iterations', type=int)
@click.option('-p1', default='ai', help='The first player (default ai)',
              type=click.Choice(['random', 'ai']))
@click.option('-p2', default='random', help='The second player (default random)',
              type=click.Choice(['random', 'ai']))
def train(iterations, p1, p2):
    """
    Function that plays through the tic-tac-toe game
    """
    game = Game()
    player_one = player_factory(p1)
    player_two = player_factory(p2)

    if iterations == 0:
        game.play_game(player_one, player_two)
    else:
        train_iterations = int(iterations * 0.9)
        for i in range(train_iterations):
            if i % 10000 == 0:
                print(f'Iteration {i} of {train_iterations}')

            game.play_game(player_one, player_two)

        print('Training complete, moving to testing')
        if hasattr(player_one, 'set_test_mode'):
            player_one.set_test_mode()
        if hasattr(player_two, 'set_test_mode'):
            player_two.set_test_mode()

        test_iterations = int(iterations * 0.1)
        for i in range(test_iterations):
            if i % 1000 == 0:
                print(f'Itreation {i} of {test_iterations}')

            game.play_game(player_one, player_two)

    if hasattr(player_one, 'display_results'):
        player_one.display_results()
    if hasattr(player_two, 'display_results'):
        player_two.display_results()

@app.command()
@click.option('--p2', is_flag=True, default=False, help='Player as player 2')
def play_game(p2):
    if p2:
        p1_type, p2_type = 'random', 'user'
    else:
        p1_type, p2_type = 'user', 'random'

    player_one = player_factory(p1_type)
    player_two = player_factory(p2_type)

    game = Game()
    game.play_game(player_one, player_two)


def player_factory(player):
    """
    Function that converts the str type to an instance of a player
    """
    if player == 'ai':
        return AIPlayer()
    if player == 'user':
        return InteractivePlayer()
    if player == 'perfect':
        return PerfectPlayer()
    if player == 'random':
        return RandomPlayer()

    raise ValueError(f'Unknown player type {player}')


if __name__ == "__main__":
    app()
    # play_game()
