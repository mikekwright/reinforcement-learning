"""
Module used for testing out the blackjack problem from chapter 5
"""
import random
import numpy as np

from collections import defaultdict
from argparse import ArgumentParser


CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
DECK = CARDS * 4

fig = None

class BlackJack:
    def __init__(self, infinite_deck=False):
        self._in_game = False
        self._player_hand = []
        self._dealer_hand = []
        self._infinite_deck = infinite_deck

    def _get_card(self):
        if self._infinite_deck:
            return random.choice(DECK)
        else:
            return self._deck.pop()

    def _init_game(self):
        if not self._infinite_deck:
            self._deck = list(DECK)
            random.shuffle(self._deck)

        self._dealer_hand = [self._get_card(), self._get_card()]
        self._player_hand = [self._get_card(), self._get_card()]

    def _run_players_turn(self, player):
        move = player.make_move(self._player_hand, self._dealer_hand[0])
        while move == 'H':
            self._player_hand.append(self._get_card())
            player_value = BlackJack.hand_value(self._player_hand)
            if player_value > 21:
                break
            move = player.make_move(self._player_hand, self._dealer_hand[0])

        return BlackJack.hand_value(self._player_hand)

    def play_game(self, player):
        self._init_game()

        player.start_game(self._player_hand, self._dealer_hand[0])
        player_value = self._run_players_turn(player)

        if player_value <= 21:
            self._play_dealer()

        reward = self.determine_reward()
        player.result(self._player_hand, self._dealer_hand, reward)

    def determine_reward(self):
        player_value = BlackJack.hand_value(self._player_hand)
        dealer_value = BlackJack.hand_value(self._dealer_hand)
        if player_value > 21:
            # Player loss on bust
            reward = -1
        elif player_value <= 21 and dealer_value > 21:
            # Player win on dealer bust
            reward = 1
        elif player_value == dealer_value:
            # They tie on score
            reward = 0
        elif player_value > dealer_value:
            # Player has higher score
            reward = 1
        else:
            # Dealer has higher score
            reward = -1

        return reward

    def _play_dealer(self):
        while BlackJack.hand_value(self._dealer_hand) < 17:
            self._dealer_hand.append(self._get_card())

    @staticmethod
    def hand_value(hand, return_scores=False):
        scores = []
        for c in hand:
            scores.append(BlackJack.card_value(c))

        score = sum(scores)
        prev_score = None
        while score > 21 and prev_score != score:
            prev_score = score
            for i in range(len(scores)):
                if scores[i] == 11:
                    scores[i] = 1
                    score = sum(scores)
                    break

        if return_scores:
            return scores
        else:
            return score

    @staticmethod
    def card_value(card):
        if card.isdigit():
            return int(card)

        if card == 'J' or card == 'Q' or card == 'K':
            return 10

        return 11


class UserBlackJackPlayer:
    def start_game(self, hand, dealer_card):
        pass

    def make_move(self, hand, dealer_card):
        print(f'Your hand: {hand} -- Dealer: [{dealer_card}, *]')
        print('What is your move? (H, S)', end=' ')

        move = input()
        while move != 'H' and move != 'S':
            print('Invalid option, please pick either H or S.', end=' ')
            move = input()

        return move

    def result(self, hand, dealer_hand, reward):
        print(f'Game over, your hand {hand} -- dealer hand {dealer_hand}')
        if reward == -1:
            print('Sorry, you lose')
        elif reward == 0:
            print("It's a draw")
        elif reward == 1:
            print('Congrats you win')
        else:
            print('Something odd happened')


class AIBlackJackPlayer:
    """
    This is an BlackJack player with policy (hit on anything not 20 or 21)
    """
    def __init__(self):
        self._values = defaultdict(list)
        self._game_moves = []

    def start_game(self, hand, dealer_card):
        self._game_moves = []

    def make_move(self, hand, dealer_card):
        usable_ace = 11 in BlackJack.hand_value(hand, return_scores=True)
        hand_value = BlackJack.hand_value(hand)

        move = None
        if hand_value != 20 and hand_value != 21:
            move = 'H'
        else:
            move = 'S'
        # move = random.choice(['H', 'S'])

        self._game_moves.append((hand_value, BlackJack.card_value(dealer_card), usable_ace))
        return move

    def result(self, hand, dealer_hand, reward):
        for move in self._game_moves:
            self._values[move].append(reward)


def render(data, useable_ace=False, plot=111, title='Plot'):
    ax = fig.add_subplot(plot, projection='3d')
    ax.set_title(title)

    X, Y, Z, = [], [], []
    for dealer in range(2, 11):
        for hand_value in range(12, 22):
        # for hand_value in range(4, 22):
            Y.append(hand_value)
            X.append(dealer)
            Z.append(np.mean(data[(hand_value, dealer, useable_ace)]))

    ax.plot_trisurf(X, Y, Z)

def run_experiment(count=500000):
    global fig

    import matplotlib
    matplotlib.use('TkAgg')

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()

    game = BlackJack(infinite_deck=True)
    player = AIBlackJackPlayer()
    for i in range(500000):
        if i % 10000 == 0:
            if i == 10000:
                render(player._values, useable_ace=True, plot=221, title='10000 Usable Ace')
                render(player._values, useable_ace=False, plot=223, title='10000 No Usable')

            print(f'Playing game {i}')
        game.play_game(player)

    render(player._values, useable_ace=True, plot=222, title='500000 Usable Ace')
    render(player._values, useable_ace=False, plot=224, title='500000 No Usable')
    plt.show()

def play_as_user():
    game = BlackJack()
    player = UserBlackJackPlayer()
    game.play_game(player)

def get_args():
    parser = ArgumentParser()
    parser.add_argument('--user', action='store_true', default=False, help='Play as a user')

    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    if args.user:
        play_as_user()
    else:
        run_experiment()
