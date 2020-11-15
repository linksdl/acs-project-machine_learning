# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project : acs-project-machine_learning      
@File    : neural networks.py
@Author  : Billy Sheng 
@Contact : shengdl999links@gmail.com  
@Date    : 2020/11/15 11:28 上午
@Version  : 1.0.0
@License : Apache License 2.0
@Desc    : None
"""

# A typical training procedure for a neural network is as follows:
#
# 1. Define the neural network that has some learnable parameters (or weights)
# 2. Iterate over a dataset of inputs
# 3. Process input through the network
# 4. Compute the loss (how far is the output from being correct)
# 5. Propagate gradients back into the network’s parameters
# 6. Update the weights of the network, typically using a simple update rule:
# weight = weight - learning_rate * gradient


import torch
import torch.nn as nn
import torch.nn.functional as F


# Define the network

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()

        # 1 input image channel, 6 output channels, 3x3 square convolution kernel
        self.conv1 = nn.Conv2d(1, 6, 3)
        self.conv2 = nn.Conv2d(6, 16, 3)

        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 6 * 6, 120)  # 6*6 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = self.conv1(x)
        x = F.relu(x)
        x = F.max_pool2d(x, (2, 2))

        # If the size is a square you can only specify a single number
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)

        x = x.view(-1, self.num_flat_features(x))

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        x = self.fc3(x)

        return x

    def num_flat_features(self, x):
        # all dimensions except the batch dimension
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s

        return num_features


net = Net()
print(net)


params = list(net.parameters())

for p in params:
    print(p.size())


input = torch.randn(1, 1, 32, 32)
print(input)
out = net(input)
print(out)

# net.zero_grad()
# out.backward(torch.randn(1, 10))

# a dummy target, for example
target = torch.randn(10)
# make it the same shape as output
target = target.view(1, -1)

criterion = nn.MSELoss()
loss = criterion(out, target)
print(loss)

# input -> conv2d -> relu -> maxpool2d -> conv2d -> relu -> maxpool2d
#       -> view -> linear -> relu -> linear -> relu -> linear
#       -> MSELoss
#       -> loss


# print(loss.grad_fn)  # MSELoss
# print(loss.grad_fn.next_functions[0][0])  # Linear
# print(loss.grad_fn.next_functions[0][0].next_functions[0][0])  # ReLU

net.zero_grad()
print('conv1.bias.grad before backward')
print(net.conv1.bias.grad)

loss.backward()
print('conv1.bias.grad after backward')
print(net.conv1.bias.grad)


learning_rate = 0.01
for f in net.parameters():
    f.data.sub(f.grad.data * learning_rate)

import torch.optim as optim
print(net.conv1.bias.grad)

# create your optimizer
optimizer = optim.SGD(net.parameters(), lr=0.01)

# in your training loop:
optimizer.zero_grad()  # zero the gradient buffers
output = net(input)
loss = criterion(output, input)
loss.backward()
optimizer.step()  # Does the update






