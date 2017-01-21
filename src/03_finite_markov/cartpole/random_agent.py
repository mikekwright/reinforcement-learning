import curses
import atexit
import time
import random
import numpy as np

from .display import Display

"""
Past experiments
 - seed: 40901, pass: 12, param: [0.45849677 -0.2585878   0.9267138   0.21173648]
 - seed: 69869, pass: 23, param: [0.02907928 -0.94252346  0.89772826  0.7489262]
 - seed: 40028, pass: 51, param: [0.15662592  0.28585267  0.85817172  0.77247924]
"""
class CartPoleAgent:
    def __init__(self, display=Display(), seed=int(random.random()*100000)):
        self.__action_count = 0
        self.__seed = seed
        self.d = display
        self.best_reward = 0
        self.best_param = None
        self.param = None
        self.__seed = seed
        np.random.seed(seed=self.__seed)

    def start_episode(self):
        self.param = np.random.rand(4) * 2 -1
        self.__action_count = 0

    def select_action(self, observation, reward, done, info):
        if done:
            self.d.print('Agent is finished, returning none for action', clear_all=True)
            return None

        self.__action_count += 1
        self.__debug(observation, reward, info)

        move_selection = np.matmul(self.param, observation)
        if move_selection < 0:
            action = 0
        else:
            action = 1

        return action

    def complete_episode(self):
        reward = self.__action_count
        if reward > self.best_reward:
            self.best_reward = reward
            self.best_param = self.param

    def display_best_results(self):
        self.d.print('Completed - best param', row=10)
        self.d.print('reward: {}'.format(self.best_reward), row=11)
        self.d.print('param: {}'.format(self.best_param), row=12)
        self.d.print('seed: {}'.format(self.__seed), row=13)
        time.sleep(5)

    def __debug(self, observation, reward, info):
        a,b,c,d = observation
        self.d.print('{}'.format(self.param), row=2)
        self.d.print('{}\t{}\t{}\t{}'.format(a,b,c,d), row=3)
        self.d.print('{}'.format(reward), row=4)
        self.d.print('{}'.format(info), row=5)
