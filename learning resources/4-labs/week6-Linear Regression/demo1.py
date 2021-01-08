# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project : acs-project-machine_learning
@File    : demo.py
@Author  : Billy Sheng
@Contact : shengdl999links@gmail.com
@Date    : 2020/11/27 7:07 下午
@Version  : 1.0.0
@License : Apache License 2.0
@Desc    : None
"""


import numpy as np
import matplotlib.pyplot as plt
import random

# w1 + w2*x + w3*x^2 + w4*x^3
x_points = []
y_points = []
y1_points = []
xset = []
yset = []
for n in range(100000):
    x = n
    x_points.append(x)
    y_points.append(n)
    y = x-(random.randint(1, 100)/100000000)
    x_ = [x, x**2, x**3]
    xset.append(x_)
    y1_points.append(y)
    yset.append([y])


inputs = np.array(xset)
targets = np.array(yset)

inputs = np.concatenate((np.ones((np.shape(inputs)[0], 1)),inputs), axis=1)
q_matrix = np.dot(np.transpose(inputs),inputs)

q_inverse = np.linalg.inv(q_matrix)

q_pseudo = np.dot(q_inverse,np.transpose(inputs))

weights = np.dot(q_pseudo,targets)
print(weights)





