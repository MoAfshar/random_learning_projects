import gym
import random
import numpy as np

class HillClimbingAgent():
    def __init__(self, env):
        self.state_dim = env.observation_space.shape # 4 dimentions
        self.action_size = env.action_space.n # 2 states
        self.build_model()

    def build_model(self):
        ## weight has to be 4 by 2 as we will multiply this by 1 by 4 to get
        ## matrix of 1 x 2 probability matrix of best action
        self.weights = 1e-4 * np.random.rand(*self.state_dim, self.action_size)  ## 1e-4 1x10^-4,
        self.best_reward = -(np.inf)
        self.best_weights = np.copy(self.weights)
        self.noise = 1e-2

    def get_action(self, state):
        # action = random.choice(range(self.action_size))
        ## return an action 0 or 1, multiply state by best weights, take highest probability
        prob = np.dot(state, self.weights)
        action = np.argmax(prob)
        return action

    def update_model(self, reward):
        if reward >= self.best_reward:
            self.best_reward = reward
            self.best_weights = np.copy(self.weights)
            ## To control our weights so they dont become too small/huge
            self.noise = max(self.noise/2, 1e-3)
        else:
            ## To control our weights so they dont become too small/huge
            self.noise = min(self.noise*2, 2)
        self.weights = self.best_weights + self.noise * np.random.rand(*self.state_dim, self.action_size)

if __name__ == '__main__':
    env_name = 'CartPole-v0'
    env = gym.make(env_name)
    print("Observation space:", env.observation_space) ## 4 values, position, velocity, angle and pole velocity at tip
    print("Action space:", env.action_space) ## 2 discrete actions, left and right

    agent = HillClimbingAgent(env)
    num_eps = 10
    for ep in range(num_eps):
        state = env.reset() ## get the intial state
        total_reward = 0
        done = False
        while not done:
            action = agent.get_action(state)
            state, reward, done, _ = env.step(action)
            env.render()
            total_reward += reward
        agent.update_model(total_reward)
        print("Episode: {}, Total Reward: {:.2f}".format(ep, total_reward))
