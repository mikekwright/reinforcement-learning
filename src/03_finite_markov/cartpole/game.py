import gym

from .random_agent import CartPoleAgent
from .display import Display


class CartPoleGame:
    def __init__(self):
        self.__env = None
        self.__agent = None
        self.d = Display(use_curses=True)
        # self.d = Display(use_curses=False)

    def train(self, passes=10):
        self.__init_env()
        env = self.__env
        agent = self.__agent

        solved = False
        i = 0
        while not solved:
            i += 1
            self.d.print('Running pass {}'.format(i), row=0)

            env.reset()
            agent.start_episode()

            done = False
            observation = env.observation_space.sample()
            info = None
            reward = 0
            loop = 0

            while not done:
                self.d.print('Loop run {}'.format(loop), row=1)
                action = agent.select_action(observation, reward, done, info)
                env.render()
                observation, reward, done, info = env.step(action)
                loop += 1
                if loop > 1000:
                    solved = True
                    break
            agent.complete_episode()

        self.d.free_curses()
        agent.display_best_results()

    def play(self):
        env = self.__load_env()

    def __init_env(self):
        if self.__env is not None:
            return

        env = gym.make('CartPole-v0')
        env.reset()
        self.__env = env
        self.__actions = [0, 1] # Grab from the env.action_space
        self.__agent = CartPoleAgent(display=self.d)


if __name__ == '__main__':
    game = CartPoleGame()
    game.train()
