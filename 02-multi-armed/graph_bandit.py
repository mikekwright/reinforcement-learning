"""
This module contains the plotting code for rendering the results of the k-armed bandit
"""
import numpy as np
import matplotlib.pyplot as plt


class KArmedBanditPlot:
    def __init__(self, policy_count=1):
        self._policy_count = policy_count
        self._next_id = 0
        self._plt = None

    def init(self):
        self._plt = plt
        self._plt.ylabel('Avg Reward')
        self._plt.xlabel('Steps')

    def add_policy(self, policy, runs, steps=1000):
        X = [0]
        for s in range(1, steps+1):
            run_averages = []
            for r in runs:
                step_reward = r[:s]
                run_averages.append(np.mean(step_reward))
            X.append(np.mean(run_averages))

        self._plt.plot(X)

    def render(self):
        self._plt.show()
