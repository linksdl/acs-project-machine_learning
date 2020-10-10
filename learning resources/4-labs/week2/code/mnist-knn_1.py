# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project : acs-project-machine_learning      
@File    : mnist-knn_1.py
@Author  : Daolin Sheng 
@Contact : shengdl999links@gmail.com  
@Date    : 2020/10/6 4:03 下午
@Version  : 1.0.0
@License : Apache License 2.0
@Desc    : None
"""

import pickle, gzip
import numpy as np
import matplotlib.pyplot as plt

with gzip.open('mnist.pkl.gz', 'rb') as f:
    train, valid, test = pickle.load(f, encoding='latin1')

# print(test[1])

# (50000, 784) (10000, 784) (10000, 784)
# print(train[0].shape, valid[0].shape, test[0].shape)

# plt.imshow(train[0][3, ].reshape(28, 28), cmap='gray_r')
# plt.show()

# fig, axs = plt.subplots(2, 5)
# for i, ax in enumerate(axs.flatten()):
#     im_idx = np.argwhere(test[1] == i)[0]
#     ax.imshow(test[0][im_idx].reshape(28, 28), cmap='gray_r')
#
# plt.show()


# the train data set
train_batch = 10000
x_train = train[0][:train_batch, :]
y_train = train[1][:train_batch]

# the test data set
test_batch = 1000
x_test = test[0][:test_batch, :]
y_test = test[1][:test_batch]


def compute_distances(xtrain, xtest):
    num_test = xtest.shape[0]
    num_train = xtrain.shape[0]
    distances = np.zeros((num_test, num_train))

    # Compute the L2 distance

    # the first method of using for loops:
    # for i in range(num_test):
    #     for j in range(num_train):
    #         # distances[i][j] = np.sqrt(np.sum((xtest[i]-xtrain[j])**2, axis=1))
    #         distances[i][j] = np.sqrt(np.sum(np.square(xtest[i] - xtrain[j])))

    # the second method :
    # for i in range(num_test):
    #     # distance = np.sqrt(np.sum(np.square(xtest[i,:] - xtrain[:]), axis=1))
    #     # distances[i, :] = distance
    #
    #     distances[i] = np.sqrt(np.sum(np.square(xtest[i] - xtrain), axis=1))

    # the third method:
    d1 = -2 * np.dot(xtest, xtrain.T)
    d2 = np.sum(np.square(xtest), axis=1, keepdims=True)
    d3 = np.sum(np.square(xtrain), axis=1)

    distances = np.sqrt(d1 + d2 + d3)

    return distances


# distances = compute_distances(x_train, x_test)
# print(distances)


# implement the predict
def predict(ytrain, distances, k=1):
    num_test = distances.shape[0]
    y_pred = np.zeros(num_test, dtype=np.dtype(int))

    for i in range(num_test):
        closest_y = []
        indics = np.argsort(distances[i])
        closest_y = ytrain[indics[:k]]

        # count = 0
        # label = 0
        # for j in closest_y:
        #     tmp = 0
        #     for kk in closest_y:
        #         tmp += (kk == j)
        #         if tmp > count:
        #             count = tmp
        #             label = j
        # y_pred[i] = label

        y_pred[i] = np.argmax(np.bincount(closest_y))

    return y_pred


def compute_accuracy(train_set, test_set, k=1):
    dists = compute_distances(train_set, test_set)
    y_pred = predict(y_train, dists, k)
    # print(y_pred)

    num_test = y_test.shape[0]
    num_correct = np.sum(y_pred == y_test)
    accuracy = float(num_correct / num_test)

    print('When the k equal to the ', k, ', the accuracy is:', accuracy * 100, '%')
    return accuracy


k_values = [1, 3, 5, 10, 100]

for k in k_values:
    accuracy = compute_accuracy(x_train, x_test, k)

np.invert()