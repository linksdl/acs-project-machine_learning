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

# y = w1 + w2 * x
# creating the input and target in numpy arrays
# inputs = np.array([[-2.0], [-1.0], [0], [1], [2]])
# targets = np.array([[-1.9], [-1.2], [0.1], [0.7], [1.7]])
#
#
# inputs = np.concatenate((np.ones((np.shape(inputs)[0],1)),inputs),axis=1)
# q_matrix = np.dot(np.transpose(inputs),inputs)
#
# q_inverse = np.linalg.inv(q_matrix)
#
# q_pseudo = np.dot(q_inverse,np.transpose(inputs))
#
# weights = np.dot(q_pseudo,targets)
# print(weights)


# w1 + w2*x + w3*x^2
# inputs = np.array([[-2.0, 4], [-1.0, 1], [0, 0], [1, 1], [2, 4]])
# targets = np.array([[-1.9], [-1.2], [0.1], [0.7], [1.7]])
#
#
# inputs = np.concatenate((np.ones((np.shape(inputs)[0],1)),inputs),axis=1)
# q_matrix = np.dot(np.transpose(inputs),inputs)
#
# q_inverse = np.linalg.inv(q_matrix)
#
# q_pseudo = np.dot(q_inverse,np.transpose(inputs))
#
# weights = np.dot(q_pseudo,targets)
# print(weights)

# w1 + w2*x^2 + w3*x^4
# inputs = np.array([[4, 16], [1, 1], [0, 0], [1, 1], [4, 16]])
# targets = np.array([[-1.9], [-1.2], [0.1], [0.7], [1.7]])
#
#
# inputs = np.concatenate((np.ones((np.shape(inputs)[0], 1)),inputs), axis=1)
# q_matrix = np.dot(np.transpose(inputs),inputs)
#
# q_inverse = np.linalg.inv(q_matrix)
#
# q_pseudo = np.dot(q_inverse,np.transpose(inputs))
#
# weights = np.dot(q_pseudo,targets)
# print(weights)

# w1 + w2*x + w3*x^2 + w4*x^3 + w5*x^4
inputs = np.array([[-2, 4, -8, 16], [-1, 1, -1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [2, 4, 8, 16]])
targets = np.array([[-1.9], [-1.2], [0.1], [0.7], [1.7]])

inputs = np.concatenate((np.ones((np.shape(inputs)[0], 1)),inputs), axis=1)
q_matrix = np.dot(np.transpose(inputs),inputs)

q_inverse = np.linalg.inv(q_matrix)

q_pseudo = np.dot(q_inverse,np.transpose(inputs))

weights = np.dot(q_pseudo,targets)
print(weights)

xset = [-2.0, -1.0, 0, 1, 2]
y = [-1.9, -1.2, 0.1, 0.7, 1.7]
y1 = [-0.12 + 0.91*x for x in xset] # y = w1 + w2 * x
y2 = [-0.10571429 + 0.91*x - 0.00714286 * x**2 for x in xset] # w1 + w2*x + w3*x^2
y3 = [0.1 - 0.45*x**2 + 0.1 * x**4 for x in xset] # w1 + w2*x^2 + w3*x^4
y4 = [0.1 + 0.96666667*x - 0.45*x**2 - 0.01666667*x**3 +0.1*x**4 for x in xset ] # w1 + w2*x + w3*x^2 + w4*x^3 + w5*x^4
plt.plot(xset, y, 'ob')
# plt.plot(xset, y1)
# plt.plot(xset, y2)
plt.plot(xset, y3)
plt.plot(xset, y4)
plt.show()


