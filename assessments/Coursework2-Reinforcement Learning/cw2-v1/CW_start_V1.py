from __future__ import division
import gym
from gym.envs.registration import register
import numpy as np
import random, math, time
import copy
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

register(
    id='FrozenLakeNotSlippery-v0',
    entry_point='gym.envs.toy_text:FrozenLakeEnv',
    kwargs={'map_name': '8x8', 'is_slippery': False},
)


def running_mean(x, N=20):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


class Agent:
    def __init__(self, env):
        self.stateCnt = env.observation_space.n
        self.actionCnt = env.action_space.n  # left:0; down:1; right:2; up:3
        self.learning_rate = 0.01
        self.gamma = 0.99
        self.epsilon = 0.9
        self.Q = self._initialiseModel()

    def _initialiseModel(self):
        # init the Q_table for all (s, a) value is 0.5.
        q_table = np.ones((self.stateCnt, self.actionCnt)) * 0.5
        return q_table

    def predict_value(self, s):

        return self.Q[s, :]

    def update_value_Q(self, s, a, r, s_next, done):
        # update the Q-table
        predict_Q = self.Q[s, a]
        if done:
            self.Q[s, a] += self.learning_rate * (r - predict_Q)
        else:
            self.Q[s, a] += self.learning_rate * (r + (self.gamma * np.max(self.Q[s_next, :])) - predict_Q)

    def update_value_S(self, s, a, r, s_next, a_next, done):
        # update the Q-table
        predict_Q = self.Q[s, a]
        if done:
            self.Q[s, a] += self.learning_rate * (r - predict_Q)
        else:
            self.Q[s, a] += self.learning_rate * (r + (self.gamma * self.Q[s_next, a_next]) - predict_Q)

    def choose_action(self, s):
        if np.random.rand() < self.epsilon:
            action = np.random.choice(self.actionCnt)
        else:
            action = np.argmax(self.Q[s, :])
        return action

    def updateEpsilon(self, episode_counter):
        # update the Epsilon value smaller, exploitation -> exploration.
        self.epsilon = self.epsilon / (1 + 0.1 * episode_counter)


class World:
    def __init__(self, env):
        self.env = env
        print('Environment has %d states and %d actions.' % (self.env.observation_space.n, self.env.action_space.n))
        self.stateCnt = env.observation_space.n
        self.actionCnt = env.action_space.n
        self.maxStepsPerEpisode = 2500
        self.q_Sinit_progress = np.array([[0.5, 0.5, 0.5, 0.5]])  # ex: np.array([[0,0,0,0]])

    def run_episode_qlearning(self):
        s = self.env.reset()  # "reset" environment to start state
        r_total = 0
        episodeStepsCnt = 0
        success = False
        for i in range(self.maxStepsPerEpisode):
            if i == 0:
                self.q_Sinit_progress = np.append(self.q_Sinit_progress, np.array([agent.Q[s]]), axis=0)
            a = agent.choose_action(s)
            s_next, r, done, info = self.env.step(a)
            r_total += r
            episodeStepsCnt += 1
            # Update the Q-table value using Q-learning algorithm
            agent.update_value_Q(s, a, r, s_next, done)
            s = s_next
            if done:
                if s_next == 63:
                    success = True
                break
            # self.env.step(a): "step" will execute action "a" at the current agent state and move the agent to the
            # nect state. step will return the next state, the reward, a boolean indicating if a terminal state is
            # reached, and some diagnostic information useful for debugging. self.env.render(): "render" will print
            # the current enviroment state. self.q_Sinit_progress = np.append( ): use q_Sinit_progress for monitoring
            # the q value progress throughout training episodes for all available actions at the initial state.
        return r_total, episodeStepsCnt, success

    def run_episode_sarsa(self):
        s = self.env.reset()  # "reset" environment to start state
        r_total = 0
        episodeStepsCnt = 0
        success = False
        a = agent.choose_action(s)
        for i in range(self.maxStepsPerEpisode):
            if i == 0:
                self.q_Sinit_progress = np.append(self.q_Sinit_progress, np.array([agent.Q[s]]), axis=0)

            s_next, r, done, info = self.env.step(a)
            a_next = agent.choose_action(s_next)
            r_total += r
            episodeStepsCnt += 1
            # Update the Q-table value using SARSA-learning algorithm
            agent.update_value_S(s, a, r, s_next, a_next, done)
            s = s_next
            a = a_next
            if done:
                if s_next == 63:
                    success = True
                break
            # self.env.step(a): "step" will execute action "a" at the current agent state and move the agent to the
            # nect state. step will return the next state, the reward, a boolean indicating if a terminal state is
            # reached, and some diagnostic information useful for debugging. self.env.render(): "render" will print
            # the current enviroment state. self.q_Sinit_progress = np.append( ): use q_Sinit_progress for monitoring
            # the q value progress throughout training episodes for all available actions at the initial state
        return r_total, episodeStepsCnt, success

    def run_evaluation_episode(self):
        agent.epsilon = 0
        self.run_episode_qlearning()
        # self.run_episode_sarsa()


if __name__ == '__main__':
    env = gym.make('FrozenLakeNotSlippery-v0')
    world = World(env)
    agent = Agent(env)  # This will creat an agent
    r_total_progress = []
    episodeStepsCnt_progress = []
    nbOfTrainingEpisodes = 1000
    for i in range(nbOfTrainingEpisodes):
        print('\n========================\n   Episode: {}\n========================'.format(i))
        # run_episode_qlearning or run_episode_sarsa
        r_total, episodeStepsCnt, success = world.run_episode_qlearning()
        # r_total, episodeStepsCnt, success = world.run_episode_sarsa()

        # append to r_total_progress and episodeStepsCnt_progress
        episodeStepsCnt_progress.append(episodeStepsCnt)
        r_total_progress.append(r_total)
        agent.updateEpsilon(i)

    # run_evaluation_episode
    world.run_evaluation_episode()


    ### --- Plots --- ###
    # 1) plot world.q_Sinit_progress
    fig1 = plt.figure(1)
    plt.ion()
    plt.plot(world.q_Sinit_progress[:, 0], label='left', color='r')
    plt.plot(world.q_Sinit_progress[:, 1], label='down', color='g')
    plt.plot(world.q_Sinit_progress[:, 2], label='right', color='b')
    plt.plot(world.q_Sinit_progress[:, 3], label='up', color='y')
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(prop=fontP, loc=1)
    plt.pause(0.001)

    # 2) plot the evolution of the number of steps per successful episode throughout training. A successful episode
    # is an episode where the agent reached the goal (i.e. not any terminal state)
    fig2 = plt.figure(2)
    plt1 = plt.subplot(1, 2, 1)
    plt1.set_title("Number of steps per successful episode")
    plt.ion()
    plt.plot(episodeStepsCnt_progress)
    plt.pause(0.0001)
    # 3) plot the evolution of the total collected rewards per episode throughout training. you can use the
    # running_mean function to smooth the plot
    plt2 = plt.subplot(1, 2, 2)
    plt2.set_title("Rewards collected per episode")
    plt.ion()
    r_total_progress = running_mean(r_total_progress)
    plt.plot(r_total_progress)
    plt.pause(0.0001)
    ### --- ///// --- ###
