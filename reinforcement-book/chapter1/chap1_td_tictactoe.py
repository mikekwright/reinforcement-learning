'''
Created on Jun 27, 2017

@author: brjones

Sutton book Chapter 1
TD learning for Tic-Tac-Toe against random player
'''

from collections import defaultdict

import numpy as np


class Board:

    def __init__(self):
        self.board = np.zeros((3,3)) # 1, -1, 0
        self.curr_player = 1         # 1, -1

    def current_player(self):
        '''
        returns: 1 for player1, -1 for player2
        '''
        return self.curr_player

    def take_action(self, row_col):
        '''
        raises Exception on illegal action or invalid row/col
        '''
        row, col = row_col
        if self.board[row, col] != 0:
            raise Exception('Illegal action')
        self.board[row, col] = self.curr_player
        self.curr_player *= -1

    def undo_action(self, row_col):
        row, col = row_col
        self.board[row, col] = 0
        self.curr_player *= -1

    def legal_actions(self):
        '''
        returns: list of (row,col) tuples
        '''
        rows, cols = np.where(self.board == 0)
        return list(zip(rows, cols))

    def legal_action_count(self):
        '''
        returns: int between 0 and 9 inclusive
        '''
        return len(self.legal_actions())

    def check_winnner(self):
        '''
        returns: 1 if player1 has won, -1 if player2 has won, 0 otherwise
        '''
        # horizontal
        h_sums = np.sum(self.board, axis=1)
        # vertical
        v_sums = np.sum(self.board, axis=0)
        # diagonals
        diag_sums = [np.sum(np.diag(self.board)),
                     np.sum(np.diag(np.fliplr(self.board)))]
        # check
        all_sums = np.concatenate([h_sums, v_sums, diag_sums])
        p1_win = 3 in all_sums
        p2_win = -3 in all_sums
        if p1_win and p2_win:
            raise Exception('Invalid board, both player 1 and player 2 have won')
        if p1_win:
            return 1
        elif p2_win:
            return -1
        else:
            return 0

    def __repr__(self):
        return 'Player: {}\nBoard:\n{}'.format(self.curr_player, self.board)

    def get_state_repr(self):
        '''
        returns: tuple of tuples representation of board
        '''
        return tuple(map(tuple, self.board))


def random_action(rng, actions):
    return actions[rng.randint(len(actions))]


class RandomPlayer:

    def __init__(self, seed=None):
        self.rng = np.random.RandomState(seed=seed)

    def get_action(self, board):
        return random_action(self.rng, board.legal_actions())

    def observe(self, board, reward):
        pass


class TDLearner:

    def __init__(self, player_num, alpha=0.1, greedy_prob=0.9, seed=None):
        self.player_num = player_num
        self.alpha = alpha
        self.greedy_prob = greedy_prob
        self.rng = np.random.RandomState(seed=seed)
        self.learning_enabled = True
        self.value_table = {} # board state -> probability of winning
        self._clear_state()

    def get_action(self, board):
        if self.player_num != board.current_player():
            raise Exception('Wrong player number')
        if not self.learning_enabled:
            return self._greedy_action(board)
        else:
            if self.rng.rand() < self.greedy_prob:
                self.last_action_greedy = True
                return self._greedy_action(board)
            else:
                self.last_action_greedy = False
                return self._random_action(board)

    def set_learning(self, enabled):
        self.learning_enabled = enabled

    def observe(self, board, reward):
        if not self.learning_enabled:
            return
        # update value table for terminal states
        is_terminal = reward != 0 or (board.legal_action_count() == 0)
        board_state = board.get_state_repr()
        if reward == 1:
            self.value_table[board_state] = 1.0 # we won, p(winning) = 1
        elif is_terminal: 
            self.value_table[board_state] = 0.0 # we lost or tied, p(winning) = 0
        # We only apply a TD update after our moves and on terminal states
        is_td_update_state = (board.current_player() != self.player_num) or is_terminal
        # Two conditions for the update
        if self.last_action_greedy and is_td_update_state:
            self._td_update(self.last_state, board_state)
        # Remember the state after one of our moves for the next update
        if board.current_player() != self.player_num:
            self.last_state = board_state
        if is_terminal:
            self._clear_state()

    def _td_update(self, last_state, new_state):
        last_value = self.value_table.get(last_state, 0.5)
        new_value = self.value_table.get(new_state, 0.5)
        self.value_table[last_state] = last_value + self.alpha * (new_value -  last_value)

    def _greedy_action(self, board):
        legal_actions = board.legal_actions()
        value_to_action_map = defaultdict(list)
        # Assess value of each action
        for action in legal_actions:
            board.take_action(action)
            new_state = board.get_state_repr()
            new_state_value = self.value_table.get(new_state, 0.5)
            board.undo_action(action)
            value_to_action_map[new_state_value].append(action)
        # Return best action, randomly selecting one in the case of a tie
        best_value = max(value_to_action_map.keys())
        return random_action(self.rng, value_to_action_map[best_value])

    def _random_action(self, board):
        return random_action(self.rng, board.legal_actions())

    def _clear_state(self):
        self.last_state = None
        self.last_action_greedy = False


def play_game(p1, p2):
    board = Board()
    winner = 0
    players = {
        1 : p1,
        -1: p2
    }
    while board.legal_action_count() > 0 and winner == 0:
        player = players[board.current_player()]
        action = player.get_action(board)
        board.take_action(action)
        winner = board.check_winnner()
        p1.observe(board, winner)
        p2.observe(board, -winner)
    return winner, board


if __name__ == '__main__':
    '''
    In this setup, the TDLearner learns only how to play as second player
    '''
    learning_game_count = 100000
    eval_game_count = 1000
    value_table_file = './value-table.txt'
    td_player = TDLearner(player_num=-1)
    rand_player = RandomPlayer()

    ###########################################################################
    # Learning phase, this is a slow process because TD(0) only backs up the 
    # value table one step at time
    print('TD Player learning...')

    td_player.set_learning(True)

    for i in range(learning_game_count):
        if i % (learning_game_count // 10) == 0:
            print('{}%, ({} / {})'.format(100 * i / learning_game_count, 
                                          i, 
                                          learning_game_count))
        play_game(rand_player, td_player)

    td_player.set_learning(False)

    ###########################################################################
    # Evaluation phase
    win_counts = defaultdict(int)
    for i in range(eval_game_count):
        winner, board = play_game(rand_player, td_player) 
        win_counts[winner] += 1

    print()
    print('Results')
    print('-'*25)
    template = '{:20}: {}'
    print(template.format('Random player win', win_counts[1]))
    print(template.format('TD learner win', win_counts[-1]))
    print(template.format('Tie', win_counts[0]))

    ###########################################################################
    # Save Value Table
    print()
    print('Writing value table to {}'.format(value_table_file))
    with open(value_table_file, 'w') as outfile:
        def sort_key(sv):
            state, value = sv
            return (np.count_nonzero(state), value)
        for state,value in sorted(td_player.value_table.items(), key=sort_key):
            print(value, file=outfile)
            print(np.array(state), file=outfile)
            print('-'*40, file=outfile)

