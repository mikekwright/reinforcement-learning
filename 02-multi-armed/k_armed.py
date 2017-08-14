"""
Module for k-Armed bandit code problem
"""
import numpy as np


def e_greedy_policy(epsilon=0.1):
    """
    A policy generator that binds an epsilon value
    """
    def _policy(action_values):
        if np.random.random() < epsilon:
            return np.random.randint(0, len(action_values))

        return np.argmax(action_values)

    return _policy


def greedy_policy(action_values):
    """
    this is a greedy policy implementation that will always pick the action
      with the highest reward
    """
    action = np.argmax(action_values)
    return action


def q_of_a(rewards):
    """
    q(a) is defined as

        sum of rewards for a over time t
        ---------------------------------
          total number of times a taken

    This is basically a mean
    """
    return rewards.mean()


class KArmedBandit:
    """
    The KArmedBandit class is a class that contians the logic around a k-armed bandit problem
      (described in README)
    """
    def __init__(self, k, true_q_of_a=None, variance=1):
        self._k = k
        self._true_q_of_a = true_q_of_a or [np.random.normal(0, 1) for i in range(k)]
        self._variance = variance
        self._reward_history = [(0, 0) for i in range(k)]
        self._step_rewards = []

    def _action_reward(self, action):
        mean = self._true_q_of_a[action]
        variance = self._variance
        return np.random.normal(mean, variance)

    def _start(self):
        self._step_rewards = []

    def _update_action_rewards(self, action, new_reward):
        reward_history = self._reward_history[action]
        last_reward = reward_history[0]
        count = reward_history[1]

        new_average = ((last_reward * count) + new_reward) / (count + 1)
        new_history = (new_average, count+1)

        self._reward_history[action] = new_history

    @property
    def values(self):
        """
        This property return the rewards for the problem
        """
        return tuple(a[0] for a in self._reward_history)

    @property
    def step_rewards(self):
        """
        This property returns the value
        """
        return tuple(self._step_rewards)

    def run(self, steps=1000, policy=greedy_policy):
        """
        The run method actual goes through the entire bandit problem for
          the number of specified steps
        """
        self._start()

        for _ in range(steps):
            action = policy(self.values)
            new_reward = self._action_reward(action)
            self._step_rewards.append(new_reward)
            self._update_action_rewards(action, new_reward)

    def display_results(self):
        """
        Used to display the standard results for the run of the k-armed bandit
        """
        print(self._reward_history)
        print(np.mean(self.step_rewards))
