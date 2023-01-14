
from numpy import sqrt, sin, cos, pi
import matplotlib.pyplot as plt
import os.path
import numpy as np
x = np.linspace(-5,5,100)
y=(x**4-13*x**2+36)/(x-3)*(x+2)
checker='y=(x**4-13*x**2+36)/(x-3)*(x+2)'
try:
    if "x" in checker:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        # plot the function
        plt.plot(x,y, 'r')
        plt.savefig('graphs/graphdraw.png')
    else:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        # plot the function
        plt.plot([y, y, y, y])
        plt.savefig('graphs/graphdraw.png')
except SyntaxError:
    os.remove("graphs/graphdraw.png")
