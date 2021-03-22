"""
pi.py by Sanjith Venkatesh
Based on video by Joma Tech: https://www.youtube.com/watch?v=pvimAM_SLic&t=421s
Script approximates pi and shows visualizations to show the dots and circle
Usage:
  pi.py <radius>
  pi.py -h | --help
"""
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from docopt import docopt
from matplotlib.animation import FuncAnimation

plt.style.use('seaborn-whitegrid')
fig1, ax1 = plt.subplots(figsize=(10,10))
fig1.set_tight_layout(True)
fig2, ax2 = plt.subplots(figsize=(12,8))
fig2.set_tight_layout(True)
rounds = 0
XYs = []
PIs = []
radius = 0
dots = 0


class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_zero(self):
        return math.sqrt(self.x**2 + self.y**2)

    def in_circle(self):
        return True if self.to_zero() < radius else False

    def printXY(self):
        print(self.x, self.y)


def average(lst):
    return reduce(lambda a, b: a + b, lst) / len(lst)


def arc_coord():
    theta = np.linspace(0, 2*np.pi, 100)

    r = radius

    x1 = r*np.cos(theta)
    x2 = r*np.sin(theta)
    return [x1, x2]


def update(i):
    global fig1
    global ax1
    global fig2
    global ax2
    global rounds

    plt.cla()

    XYs_to_use = gen_rand_coord()
    pi = approximate_pi(XYs_to_use)
    rounds += 1

    fig1.suptitle("Overall Pi value = " + str(pi))
    fig2.suptitle("Change in Overall Value of Pi")
    arc_coords = arc_coord()
    rounds_x = np.arange(0,rounds,1)
    ax1.plot(arc_coords[0], arc_coords[1], color="blue", linewidth=1)
    ax2.plot(rounds_x, PIs, color="blue", linewidth=1)
    for XY in XYs_to_use:
        if XY.in_circle():
            ax1.scatter(XY.x, XY.y, color="green")
        else:
            ax1.scatter(XY.x, XY.y, color="red")
    ax1.set_xlim(radius*-1 - (radius*0.1), radius + (radius * 0.1))
    ax1.set_ylim(radius*-1 - (radius * 0.1), radius + (radius * 0.1))


def gen_rand_coord():
    global XYs

    x = random.uniform(radius*-1, radius)
    y = random.uniform(radius*-1, radius)

    XYs.append(XY(x, y))
    return XYs


def approximate_pi(XYs):
    global PIs
    in_circle = [c for c in XYs if c.in_circle()]
    in_circle_count = len(in_circle)

    new_pi = (4 * (in_circle_count/len(XYs)))
    PIs.append(new_pi)
    return new_pi


def prepare_vars(r):
    global radius
    radius = r


if __name__ == "__main__":
    args = docopt(__doc__)

    r = int(args["<radius>"]) if args["<radius>"] is not None else 1
    prepare_vars(r)
    anim = FuncAnimation(fig1, update, interval=500)
    anim2 = FuncAnimation(fig2, update, interval=500)
    plt.show()
