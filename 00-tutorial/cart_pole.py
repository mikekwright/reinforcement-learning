import gym
import os
import shutil

from collections import defaultdict
from pprint import pprint


class CartPole:
    def __init__(self, alpha=0.1, max_count=10000):
        self._alpha = alpha
        self._max_count = max_count
        self._env = None
        self._complete = False
        self._last_state = None
        self._state_values = None

    def init(self, overwrite=False):
        results_path = os.path.join(os.path.dirname(__file__), 'pole-results')
        if not overwrite and os.path.exists(results_path):
            raise ValueError('You need to first remove the previous results, use "--overwrite"')

        if overwrite:
            shutil.rmtree(results_path)

        self._env = gym.wrappers.Monitor(gym.make('CartPole-v0'), results_path)
        self._state_values = defaultdict(lambda: 0)

    @staticmethod
    def _state_from_observation(observation, action=-1):
        return (tuple(int(i * 100) for i in observation), action)

    def run_episode(self):
        """
        Run an e

        :param param1:
        :returns:
        :raises keyError:
        """
        current_observation = self._env.reset()
        current_state = self._state_from_observation(current_observation)
        self._complete = False

        done = False
        count = 0
        while not done and count < self._max_count:
            self._env.render()
            available_actions = tuple(range(self._env.action_space.n))

            max_move = None
            for a in available_actions:
                key = self._state_from_observation(current_observation, a)
                if max_move is None or self._state_values[max_move] < self._state_values[key]:
                    max_move = (key, a)

            selected_action = max_move[1]
            # observation, reward, done, info = self._env.step(self._env.action_space.sample())
            observation, reward, done, _ = self._env.step(selected_action)
            next_state = self._state_from_observation(observation, selected_action)
            self._state_values[current_state] += self._alpha * (reward + self._state_values[next_state])
            current_state = next_state
            count += 1

        print(f'Episode complete: count {count}')
        self._state_values[current_state] = 0

        # for i, state in enumerate(visited_states):
        #     self._state_values[state] += self._alpha * (count - self._state_values[state])
            # self._state_values[max_move] += self._alpha * (reward - self._state_values[max_move])
            # print(observation, reward, done)

        if self._max_count == count:
            self._complete = True

    @property
    def complete(self):
        return self._complete

    def display_results(self):
        pprint(self._state_values)
