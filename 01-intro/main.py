import click

from tic_tac_toe import Game, RandomPlayer, PerfectPlayer, InteractivePlayer
from ai_player import AIPlayer


@click.command()
@click.option('--iterations', default=10000, help='Number of iterations to run')
@click.option('--p1-type', default='random', help='The first player',
    type=click.Choice(['random', 'user', 'ai']))
@click.option('--p2-type', default='ai', help='The second player',
    type=click.Choice(['random', 'user', 'ai']))
def play_game(iterations, p1_type, p2_type):
    """
    Function that plays through the tic-tac-toe game
    """
    if iterations > 0 and (p1_type == 'user' or p2_type == 'user'):
        print('Doing more then 1 iteration with a user is not recommended')

    player_one = player_factory(p1_type)
    player_two = player_factory(p2_type)

    game = Game()

    for i in range(iterations):
        if i % 10000 == 0:
            print(f'Iteration {i} of {iterations}')

        game.play_game(player_one, player_two)

    if hasattr(player_one, 'display_results'):
        player_one.display_results()
    if hasattr(player_two, 'display_results'):
        player_two.display_results()


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
    play_game()
