# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project : acs-project-machine_learning      
@File    : demo.py
@Author  : Billy Sheng 
@Contact : shengdl999links@gmail.com  
@Date    : 2020/12/4 4:12 下午
@Version  : 1.0.0
@License : Apache License 2.0
@Desc    : None
"""

import numpy as np

q = np.ones((64, 4))*0.5


# no left
for i in range(0, 64, 8):
    q[i][0] = 0

# no down
for i in range(56, 64, 1):
    q[i][1] = 0

# no left
for i in range(7, 64, 8):
    q[i][2] = 0

# no up
for i in range(8):
    q[i][3] = 0

print(q)


a = [1, 2, 3,5, 5]
print(np.max(a))
print(np.argmax(a))

