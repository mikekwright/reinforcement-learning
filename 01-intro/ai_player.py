"""
This module provides the implementation of the AI player that can support different policies
"""
import random
import os
import json

from collections import defaultdict


class AIPlayer:
    """
    The actual ai player
    """
    def __init__(self, alpha=0.1, exploration=0.1):
        self._state_values = defaultdict(lambda: 0)
        self._alpha = alpha
        self._exploration = exploration
        self._piece = None
        self._last_state = None
        self._test_mode = False
        self._wins = 0
        self._draws = 0
        self._losses = 0
        self._count = 0

    def start(self, piece):
        """
        Called when a new game is started
        """
        self._piece = piece

    def set_test_mode(self):
        """
        Moves the model from training to testing
        """
        self._test_mode = True
        self._wins = 0
        self._draws = 0
        self._count = 0
        self._losses = 0

    def set_exploration(self, exploration):
        """
        Ability to adjust exploration value on the fly
        """
        self._exploration = exploration

    def _update_state_value(self, old_state, new_state):
        """
        Update the state value with this operation
          * V(s) = V(s) + alpha [V(s') - V(s)]
        """
        if not self._test_mode:
            if isinstance(new_state, int):
                self._state_values[old_state] += self._alpha * \
                    (new_state - self._state_values[old_state])
            else:
                self._state_values[old_state] += self._alpha * \
                    (self._state_values[new_state] - self._state_values[old_state])

    def _get_state_for_action(self, state, action):
        return (self._piece, tuple(state[i] if i != action else self._piece
                                   for i in range(len(state))))

    def _states_from_actions(self, state, actions):
        return {a: self._get_state_for_action(state, a)
                for a in actions}

    def make_move(self, state, actions):
        """
        Called whenever a move should be made, given a list of available actions and
          a board state
        """

        # Here we are doing an exploration so don't update scores
        #  for selected state
        if random.random() < self._exploration:
            action = random.choice(actions)
            self._last_state = self._get_state_for_action(state, action)
            return action

        # So we are not doing exploration, here we want to update it
        max_selection = None
        for a, s in self._states_from_actions(state, actions).items():
            state_value = self._state_values[s]
            if max_selection is None or state_value > self._state_values[max_selection[1]]:
                max_selection = (a, s)

        if self._last_state is not None:
            self._update_state_value(self._last_state, max_selection[1])

        self._last_state = max_selection[1]
        return max_selection[0]

    def finish(self, state, score):
        """
        This method is called when the game is finished, the score is one of three values
          * 1 for win
          * 0 for draw
          * -1 for loss
        """
        self._count += 1
        if score == 1:
            self._wins += 1
        elif score == 0:
            self._draws += 1
        elif score == -1:
            self._losses += 1

        if self._last_state is not None:
            self._update_state_value(self._last_state, score)


    def display_results(self):
        """
        This is a helper method to be called at the end of a game, so that results of
          the model can be displayed
        """
        print(f'AI player results - Wins: {self._wins}, Draws: {self._draws}, Loss: {self._losses}')
        print(f'Total win percentage {(self._wins / self._count) * 100}', end='\n\n')

        with open(os.path.join(os.path.dirname(__file__), 'ai-results.json'), 'w') as f:
            output_dict = {str(k): v for k, v in self._state_values.items()}
            json.dump(output_dict, f, indent=4, sort_keys=True)
