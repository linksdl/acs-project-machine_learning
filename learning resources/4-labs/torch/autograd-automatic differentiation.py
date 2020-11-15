# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project : acs-project-machine_learning      
@File    : autograd-automatic differentiation.py
@Author  : Billy Sheng 
@Contact : shengdl999links@gmail.com  
@Date    : 2020/11/15 10:58 上午
@Version  : 1.0.0
@License : Apache License 2.0
@Desc    : None
"""

import torch

# Create a tensor and set requires_grad=True to track computation with it

x = torch.ones(2, 2, requires_grad=True)
print(x)

# Do a tensor operation:
y = x + 2
print(y)

# y was created as a result of an operation, so it has a grad_fn.
print(y.grad_fn)

z = y * y * 3
out = z.mean()
print(z, out)

a = torch.randn(2, 2)
a = ((a * 3) / (a-1))
print(a.requires_grad)
a.requires_grad_(True)
print(a.requires_grad)
b = (a * a).sum()
print(b.grad_fn)


# Gradients
# Let’s backprop now. Because out contains a single scalar,
# out.backward() is equivalent to out.backward(torch.tensor(1.)).

out.backward()
print(x.grad)

x = torch.randn(3, requires_grad=True)
print(x)
y = x * 2
while y.data.norm() < 1000:
    y = y * 2

print(y)

v = torch.tensor([0.1, 1.0, 0.0001], dtype=torch.float)
y.backward(v)
print(x.grad)




print(x.requires_grad)
print((x ** 2).requires_grad)

with torch.no_grad():
    print((x ** 2).requires_grad)



print(x.requires_grad)
y = x.detach()
print(y.requires_grad)
print(x.eq(y).all())
