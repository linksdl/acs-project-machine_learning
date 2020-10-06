# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project : acs-project-machine_learning
@File    : mnist-knn.py
@Author  : Daolin Sheng
@Contact : shengdl999links@gmail.com
@Date    : 2020/10/6 1:32 下午
@Version  : 1.0.0
@License : Apache License 2.0
@Desc    : Lab exercises about knn- MNIST dataset
"""

import pickle, gzip
import math
# pip install matplotlib
import matplotlib.pyplot as plt
import numpy as np

# load the MNIST Dataset
f = gzip.open("mnist.pkl.gz", "rb")

# preparation the dataset
train_set, validation_set, test_set = pickle.load(f, encoding="latin1")


print(train_set[0].shape, validation_set[0].shape, test_set[0].shape)
f.close()



fig, axs = plt.subplots(2, 5)
for i, ax in enumerate(axs.flatten()):
    im_idx = np.argwhere(test_set[1] == i)[0]
    plottable_image = np.reshape(test_set[0][im_idx], [28, 28])
    ax.imshow(plottable_image, cmap='gray_r')

# print(train_set)
train_read = 10000
Xtrain = train_set[0][:train_read, :]
Ytrain = train_set[1][:train_read]

# print(Ytrain)

test_read = 1000
Xtest = test_set[0][:test_read, :]
Ytest = test_set[0][:test_read, :]


def compute_distances(Xtrain, X):
    num_test = X.shape[0]
    num_train = Xtrain.shape[0]
    distances = np.zeros(num_test, num_train)

    return distances


distances = None
distances = compute_distances(Xtrain, Xtest)


def predict(ytrain, distances, k=1):
    num_test = distances.shape[0]
    y_pred = np.zeros(num_test, dtype=np.dtype(int))

    return y_pred


k = 1
y_pred = predict(Ytrain, distances, k)
y_pred[:10]

num_test = Ytest.shape[0]
num_correct = np.sum(y_pred == Ytest)
accuracy = float(num_correct / num_test)
print("Accuracy: ", accuracy * 100, '%')

k_values = [1, 3, 5, 10, 100]
