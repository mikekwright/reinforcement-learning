import gym
import os
import shutil


class CartPole:
    def __init__(self):
        self._env = None

    def init(self, overwrite=False):
        if not overwrite and os.path.exists(os.path.join(os.path.dirname(__file__), 'pole-results')):
            raise ValueError('You need to first remove the previous results or run with "--overwrite"')

        if overwrite:
            shutil.rmtree(os.path.join(os.path.dirname(__file__), 'pole-results'))

        self._env = gym.wrappers.Monitor(gym.make('CartPole-v0'), 'pole-results')

    def start(self):
        self._env.reset()

    def play_game(self):
        self._env.render()
        self._env.step(self._env.action_space.sample())
