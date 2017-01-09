from logging import debug, info
from colorama import init, Fore, Back, Style
init()


class Trainer:
    @staticmethod
    def train(iterations, plays, game, players):
        info(Fore.LIGHTYELLOW_EX + 'Strating training for {} iterations'.format(iterations) + Style.RESET_ALL)
        for iteration in range(iterations):
            info(Fore.LIGHTRED_EX + 'Running iteration {} of {}'.format(iteration+1, iterations) + Style.RESET_ALL)
            Trainer.__train_each_player(game=game, plays=plays, players=players)
            debug('Completed iteration {}'.format(iteration))
        debug('Completed all {} training iterations'.format(iterations))

    @staticmethod
    def __train_each_player(game, plays, players):
        for training_player in players:
            info(Fore.LIGHTGREEN_EX + 'Training player {}'.format(training_player.name) + Style.RESET_ALL)
            static_players = [p for p in players if p is not training_player]
            training_player.enable_training()
            for s in static_players:
                s.disable_training()
            Trainer.__run_training(game=game, plays=plays, players=players)

    @staticmethod
    def __run_training(game, plays, players):
        info(Fore.LIGHTBLUE_EX + 'Starting training plays {}'.format(plays) + Style.RESET_ALL)
        for i in range(plays):
            if i % 1000 == 0:
                info('Running train iteration {}'.format(i))
            game.play(players)

