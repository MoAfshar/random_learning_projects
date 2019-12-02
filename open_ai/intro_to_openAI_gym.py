import gym
import random

env_name = 'CartPole-v1'
env = gym.make(env_name)
print("Observation space:", env.observation_space) ## 4 values, position, velocity, angle and pole velocity at tip
print("Action space:", env.action_space) ## 2 discrete actions, left and right
## reset the environment state
env.reset()

class Agent():
    def __init__(self, env):
        self.action_size = env.action_space.n

    def get_action(self):
        action = random.choice(range(self.action_size))
        return action

for _ in range(200):
    agent = Agent(env)
    action = env.action_space.sample() ## Get a random action
    env.step(action) ## Play the action
    env.render() ##  Show the graphic
