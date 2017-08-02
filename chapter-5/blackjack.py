"""
Module used for testing out the blackjack problem from chapter 5
"""
import random
import numpy as np

from collections import defaultdict
from argparse import ArgumentParser
from pprint import pprint


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

    def _init_game(self, start_hand, dealer_hand):
        if not self._infinite_deck:
            self._deck = list(DECK)
            random.shuffle(self._deck)

        self._dealer_hand = dealer_hand or [self._get_card(), self._get_card()]
        self._player_hand = start_hand or [self._get_card(), self._get_card()]

    def _run_players_turn(self, player):
        move = player.make_move(self._player_hand, self._dealer_hand[0])
        while move == 'H':
            self._player_hand.append(self._get_card())
            player_value = BlackJack.hand_value(self._player_hand)
            if player_value > 21:
                break
            move = player.make_move(self._player_hand, self._dealer_hand[0])

        return BlackJack.hand_value(self._player_hand)

    def play_game(self, player, start_hand=None, dealer_hand=None):
        self._init_game(start_hand, dealer_hand)

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
    def __init__(self, policy=None, store_values=True):
        self._values = defaultdict(list)
        self._game_moves = []
        self._policy = policy
        self._reward = None
        self._store_values = store_values

    @property
    def reward(self):
        return self._reward

    @property
    def game_moves(self):
        return self._game_moves

    @staticmethod
    def _default_policy(hand_value, dealer_value, usable_ace):
        return random.choice(['H', 'S'])

    def start_game(self, hand, dealer_card):
        self._game_moves = []

    def make_move(self, hand, dealer_card):
        usable_ace = 11 in BlackJack.hand_value(hand, return_scores=True)
        hand_value = BlackJack.hand_value(hand)
        dealer_value = BlackJack.card_value(dealer_card)
        state = (hand_value, BlackJack.card_value(dealer_card), usable_ace)

        if not self._policy:
            move = AIBlackJackPlayer._default_policy(hand_value, dealer_value, usable_ace)
        else:
            move = self._policy(hand_value, dealer_value, usable_ace)

        self._game_moves.append((state, move))
        return move

    def result(self, hand, dealer_hand, reward):
        if self._store_values:
            for state, move  in self._game_moves:
                self._values[state].append(reward)

        self._reward = reward


def exploring_starts(iteration=200, epsilon=None):
    """
    This is the method that you use to test exploring starts with Monte Carlo
    """
    starting_states = [
        ((h, d, False), a) for h in range(12, 22)
                        for d in range(2, 11)
                        for a in ['H', 'S']
    ]
    starting_states.extend([
        ((h, d, True), a) for h in range(12, 22)
                        for d in range(2, 11)
                        for a in ['H', 'S']
    ])

    policy_values = {s: [] for s in starting_states}

    game = BlackJack(infinite_deck=True)

    for i in range(iteration):
        for start_state in starting_states:
            hand_value, dealer_value, usable_ace = start_state[0]
            action = start_state[1]

            if usable_ace:
                start_hand = [['A', h] for h in CARDS if BlackJack.hand_value(['A', h]) == hand_value][0]
            else:
                start_hand = [[h1, h2] for h1 in CARDS for h2 in CARDS if BlackJack.hand_value([h1, h2]) == hand_value][0]
            dealer_card = [d for d in CARDS if BlackJack.card_value(d) == dealer_value][0]

            def policy(*state):
                if state == start_state[0]:
                    return action

                hit_rewards = policy_values[state, 'H']
                hit_value = 0 if len(hit_rewards) == 0 else np.mean(hit_rewards)

                stay_rewards = policy_values[state, 'S']
                stay_value = 0 if len(stay_rewards) == 0 else np.mean(stay_rewards)

                if hit_value == stay_value or (epsilon and random.random() < epsilon):
                    move = random.choice(['H', 'S'])
                elif hit_value > stay_value:
                    move = 'H'
                else:
                    move = 'S'
                return move

            dealer_hand = [dealer_card, random.choice(CARDS)]
            player = AIBlackJackPlayer(policy=policy)
            game.play_game(player, start_hand=start_hand, dealer_hand=dealer_hand)

            reward = player.reward
            for state, move in player.game_moves:
                policy_values[(state, move)].append(reward)

        if i % 20 == 0:
            print(f'Iteration {i} - Game {i*len(starting_states)}')

    for p, v in policy_values.items():
        print(f'{p} - {np.mean(v)} - {len(v)}')

    import matplotlib
    matplotlib.use('TkAgg')

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()

    def render_3d(useable_ace=False, plot=111, title='Plot'):
        ax = fig.add_subplot(plot, projection='3d')
        ax.set_title(title)

        X, Y, Z, = [], [], []
        for dealer in range(2, 11):
            for hand_value in range(12, 22):
            # for hand_value in range(4, 22):
                Y.append(hand_value)
                X.append(dealer)

                hit_value = np.mean(policy_values[((hand_value, dealer, useable_ace), 'H')])
                stay_value = np.mean(policy_values[((hand_value, dealer, useable_ace), 'S')])
                Z.append(np.max([hit_value, stay_value]))

        ax.plot_trisurf(X, Y, Z)

    def render_2d(useable_ace=False, plot=111, title='Plot'):
        ax = fig.add_subplot(plot)
        ax.set_title(title)
        ax.yaxis.tick_right()

        ax.set_xlim([2, 11])
        ax.set_ylim([10, 21])

        X = range(2, 12)
        Y = []
        for x in X:
            hit = None
            for y in range(11, 22):
                hit_value = np.mean(policy_values.get(((y, x, useable_ace), 'H'), [0]))
                stay_value = np.mean(policy_values.get(((y, x, useable_ace), 'S'), [0]))

                if stay_value <= hit_value or hit is None:
                    hit = y
                else:
                    break

            Y.append(hit)

        print(X, Y)
        ax.plot(X, Y)


    render_2d(useable_ace=True, plot=221, title='Usable Policy')
    render_3d(useable_ace=True, plot=222, title='Usable Value')
    render_2d(useable_ace=False, plot=223, title='No Usable Policy')
    render_3d(useable_ace=False, plot=224, title='No Usable Value')

    plt.show()


def policy_1(count=500000):
    """
    This is the method that you use to test the value for policy 20-21H
    """
    import matplotlib
    matplotlib.use('TkAgg')

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()

    def render(data, useable_ace=False, plot=111, title='Plot'):
        ax = fig.add_subplot(plot, projection='3d')
        ax.set_title(title)

        X, Y, Z, = [], [], []
        for dealer in range(2, 12):
            for hand_value in range(12, 22):
            # for hand_value in range(4, 22):
                Y.append(hand_value)
                X.append(dealer)
                Z.append(np.mean(data[(hand_value, dealer, useable_ace)]))

        ax.plot_trisurf(X, Y, Z)

    game = BlackJack(infinite_deck=True)
    def policy(hand_value, dealer_value, usable_ace):
        move = None
        if hand_value != 20 and hand_value != 21:
            move = 'H'
        else:
            move = 'S'
        return move

    player = AIBlackJackPlayer(policy=policy)
    for i in range(count):
        if i % 10000 == 0:
            if i == 10000:
                render(player._values, useable_ace=True, plot=221, title='10000 Usable Ace')
                render(player._values, useable_ace=False, plot=223, title='10000 No Usable')

            print(f'Playing game {i}')
        game.play_game(player)

    render(player._values, useable_ace=True, plot=222, title=f'{count} Usable Ace')
    render(player._values, useable_ace=False, plot=224, title=f'{count} No Usable')
    plt.show()


def play_as_user():
    """
    This method lets you play, as a user, against the dealer
    """
    game = BlackJack()
    player = UserBlackJackPlayer()
    game.play_game(player)


def get_args():
    """
    Get the args for the user to run the system
    """
    parser = ArgumentParser()
    parser.add_argument('--user', action='store_true', default=False, help='Play as a user')
    parser.add_argument('--policy1', action='store_true', default=False, help='Run value evaluation using 20-21H policy')
    parser.add_argument('--es', action='store_true', help='Run MC with Exploring Starts')
    parser.add_argument('--greedy', dest='greedy', action='store_true', help='Run MC with Greedy' )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    if args.user:
        play_as_user()
    elif args.policy1:
        policy_1()
    elif args.es:
        exploring_starts()
    elif args.greedy:
        exploring_starts(epsilon=.1)

