"""
This module provides the implementation of the AI player that can support different policies
"""
import random


class AIPlayer:
    """
    The actual ai player
    """
    def __init__(self, policy=None):
        self._policy = policy or AIPlayer._default_policy

    @staticmethod
    def _default_policy(player, state, actions):
        return random.choice(actions)

    def start(self, piece):
        """
        Called when a new game is started
        """
        pass

    def make_move(self, state, actions):
        """
        Called whenever a move should be made, given a list of available actions and
          a board state
        """
        return self._policy(self, state, actions)

    def finish(self, state, score):
        """
        This method is called when the game is finished, the score is one of three values
          * 1 for win
          * 0 for draw
          * -1 for loss
        """
        pass

    def display_results(self):
        """
        This is a helper method to be called at the end of a game, so that results of
          the model can be displayed
        """
        pass
