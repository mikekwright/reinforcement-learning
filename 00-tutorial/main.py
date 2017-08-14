import click

from cart_pole import CartPole


@click.command()
@click.argument('episodes', type=int)
@click.option('--overwrite', is_flag=True, default=False, help='Remove previous results')
@click.option('--alpha', default=0.1, type=float, help='The alpha for the model')
def train(episodes, overwrite, alpha):

    pole = CartPole(alpha=alpha)
    pole.init(overwrite=overwrite)

    for _ in range(episodes):
        pole.run_episode()

        if pole.complete:
            break

    pole.display_results()

    if pole.complete:
        print('Congrats, you got it')
    else:
        print(f'Unable to find the solution in {episodes} episodes')


if __name__ == "__main__":
    train()
