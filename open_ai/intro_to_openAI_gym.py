import gym
import random
import numpy as np

env_name = 'CartPole-v1'
env = gym.make(env_name)
print("Observation space:", env.observation_space) ## 4 values, position, velocity, angle and pole velocity at tip
print("Action space:", env.action_space) ## 2 discrete actions, left and right

class Agent():
    def __init__(self, env):
        self.action_size = env.action_space.n

    def get_action(self, state):
        # action = random.choice(range(self.action_size)) ## return an action 0 or 1
        pole_angle = state[2]
        action = 0 if pole_angle < 0 else 1
        return action

state = env.reset() ## reset the environment state and store the intial step
for _ in range(200):
    agent = Agent(env)
    action = agent.get_action(state) ## Get a random action
    state, reward, done, info = env.step(action) ##retrurn the state, reward, whether we reached the terminal state and some additional info
    env.render() ##  Show the graphic
