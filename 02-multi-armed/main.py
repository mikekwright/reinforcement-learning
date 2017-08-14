"""
Module that runs the actual k-armed bandit problem
"""
import click
import numpy as np
from pprint import pprint

from k_armed import KArmedBandit, e_greedy_policy, greedy_policy
from graph_bandit import KArmedBanditPlot


DEFAULT_Q = [0.25, -0.8, 1.5, 0.5, 1.3, -1.5, -0.2, -1, 0.8, -0.5]

@click.command()
@click.option('--k', default=10, type=int, help='The number of arms (k)')
@click.option('--runs', default=2000, type=int, help='The number of runs to train')
@click.option('--steps', default=1000, type=int, help='The number of steps in a run')
@click.option('--rand-q', default=False, is_flag=True, help='Use a random q* value')
def run_k_armed(k, runs, steps, rand_q):
    """
    This is the actual cli command to run the k-armed bandit
    """
    q_values = None if rand_q or k != 10 else DEFAULT_Q

    policies = [
        {
            'name': 'greedy',
            'policy': greedy_policy,
            'bandit': KArmedBandit(k, q_values)
        }, {
            'name': 'e-greedy-0.1',
            'policy': e_greedy_policy(epsilon=0.1),
            'bandit': KArmedBandit(k, q_values)
        }, {
            'name': 'e-greedy-0.01',
            'policy': e_greedy_policy(epsilon=0.01),
            'bandit': KArmedBandit(k, q_values)
        },
    ]

    for r in range(runs):
        # if (r+1) % 10 == 0:
        print(f'Run {r+1} of {runs}')
        for p in policies:
            policy = p['policy']
            bandit = p['bandit']
            bandit.run(steps=steps, policy=policy)
            p.setdefault('runs', []).append(bandit.step_rewards)

    plt = KArmedBanditPlot(policy_count=len(policies))
    plt.init()
    for p in policies:
        plt.add_policy(p['name'], p['runs'], steps=steps)

    plt.render()

        # p['bandit'].display_results()
        # for s in range(1, steps+1):
        #     print(f'Step {s}:')
        #     run_averages = []
        #     for r in p['runs']:
        #         step_history = r[:s]
        #         avg_reward = np.mean(step_history)
        #         run_averages.append(avg_reward)
        #     name = p['name']
        #     print(f'Policy {name} step: {s} - avg: {np.mean(run_averages)}')


if __name__ == '__main__':
    run_k_armed()
