
from numpy import sqrt, sin, cos, pi
import matplotlib.pyplot as plt
import os.path
import numpy as np
x = np.linspace(-5,5,100)
y=sin(x)
checker='y=sin(x)'
try:
    if "x" in checker:
        fig = plt.figure()
        fig.set_facecolor("#0E1621")
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.set_facecolor("#0E1621")
        ax.xaxis.set_ticks_position('bottom')
        ax.tick_params(color='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.yaxis.set_ticks_position('left')
        # plot the function
        plt.plot(x,y, 'r')
        plt.savefig("users/1018846041/graphdraw.png")
    else:
        fig = plt.figure()
        fig.set_facecolor("#0E1621")
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['bottom'].set_position('zero')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.set_facecolor("#0E1621")
        ax.xaxis.set_ticks_position('bottom')

        ax.yaxis.set_ticks_position('left')
        # plot the function
        plt.plot([y, y, y, y])
        plt.savefig("users/1018846041/graphdraw.png")
except SyntaxError:
    print("ok")
