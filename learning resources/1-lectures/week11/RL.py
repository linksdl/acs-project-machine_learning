# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project : acs-project-machine_learning      
@File    : RL.py
@Author  : Billy Sheng 
@Contact : shengdl999links@gmail.com  
@Date    : 2021/1/20 1:03 下午
@Version  : 1.0.0
@License : Apache License 2.0
@Desc    : None
"""

import numpy as np

q = np.matrix(np.zeros([4,4]))

r = np.matrix([[1000, -2, -1, 1000],
               [1000, 1000, 0,  0],
               [1000, 0, 1000,  0],
               [0,  1000,  1000, 1000]])

# hyperparameter
gamma = 0
epsilon = 0.1

# the main training loop
for episode in range(201):
    # random initial state
    state = np.random.randint(0, 4)

    while state != 3:  # stop only when state == TERMINAL
        # Filter feasible actions.
        # Even in random case, we cannot choose actions whose r[state, action] = -1.
        # It's not about reinforcement learning. These actions are not feasible physically.
        possible_actions = []
        possible_q = []
        for action in range(4):
            if r[state, action] != 1000:
                possible_actions.append(action)
                possible_q.append(q[state, action])

        # Step next state, here we use epsilon-greedy algorithm.
        action = -1
        if np.random.random() < epsilon:
            # choose random action
            action = possible_actions[np.random.randint(0, len(possible_actions))]
        else:
            # greedy
            action = possible_actions[np.argmax(possible_q)]

        # Update Q value
        q[state, action] = r[state, action] + gamma * q[action].max()

        # Go to the next state
        state = action

    # Display training progress
    if episode % 10 == 0:
        print("------------------------------------------------")
        print("Training episode: %d" % episode)
        print(q)
