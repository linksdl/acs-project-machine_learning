# !/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Project : acs-project-machine_learning      
@File    : k-nearest-neighbour-example.py
@Author  : Daolin Sheng 
@Contact : shengdl999links@gmail.com  
@Date    : 2020/10/6 10:26 上午
@Verion  : 1.0.0
@License : Apache License 2.0
@Desc    : The Machine Learning KNN demo
'''

import numpy as np

# The
X_train = np.array([[1, 6], [2, 2], [3, 7], [5, 4], [6, 8], [6, 1], [7, 5]])

print(X_train)

# Character
Y_train = np.array([0, 0, 0, 1, 1, 1, 1])

# target point
x = np.array([[1, 2]])

distences = np.sqrt(np.sum((X_train-x) ** 2, axis=1))

print(distences)

# np.argsort for the mix to max. Returns the indices that would sort an array.
indices  = np.argsort(distences,axis=0)

print(indices)


k = 3

closest_y = Y_train[indices[:k]]

print(closest_y)

print(np.bincount(closest_y))
y_pred  = np.argmax(np.bincount(closest_y))
print(y_pred)

