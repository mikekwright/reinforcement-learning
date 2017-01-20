import universe
import gym

env = gym.make('gym-core.CartPole-v0')
print(env)
print(env.action_space)
print(env.observation_space)
quit()


env.configure(remotes=1)
observation_n = env.render()

for i_episode in range(20):
    observation = env.reset()
    print(observation)
    for t in range(100):
        env.render()
        print(observation)
        action = env.action_space.sample()
        print(action)
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
