import click

from cart_pole import CartPole


@click.command()
@click.argument('episodes', type=int)
@click.option('--overwrite', is_flag=True, default=False, help='Remove previous results')
def train(episodes, overwrite):

    pole = CartPole()
    pole.init(overwrite=overwrite)

    pole.start()

    for _ in range(episodes):
        pole.play_game()


if __name__ == "__main__":
    train()
