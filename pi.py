"""
pi.py by Sanjith Venkatesh
Based on video by Jorma Tech: https://www.youtube.com/watch?v=pvimAM_SLic&t=421s
Script approximates pi and shows visualizations to show the dots and circle
Usage:
  pi.py <radius> <dots> <rounds>
  pi.py -h | --help
"""
import math
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from docopt import docopt


class XY:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def to_zero(self):
        return math.sqrt(self.x**2 + self.y**2)

    def in_circle(self, radius):
        return True if self.to_zero() < radius else False

def average(lst):
    return reduce(lambda a, b: a + b, lst) / len(lst)

def arc_coord(radius):
    P1 = XY(0,1)
    theta = np.linspace(0,90,9000)
    x = []
    y = []
    for angle in theta:
        x.append(P1.x + radius*math.sin(angle))
        y.append(P1.y - radius*(1-math.cos(angle)))
    return {"x": x, "y": y}


def plot_simulation(radius, XYs, pis):
    num_cols = 2
    num_rows = math.ceil(len(XYs)/num_cols)
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(10,8))

    fig.suptitle("Overall Pi value = " + str(average(pis)))
    arc_coords = arc_coord(radius)
    spot = 0
    for row in range(0,num_rows):
        for col in range(0,num_cols):
            if spot < len(XYs):
                axs[row,col].plot(arc_coords["x"], arc_coords["y"], color="blue", linewidth=5)

                for XY in XYs[spot]:
                    if XY.in_circle(radius):
                        axs[row,col].scatter(XY.x, XY.y, color="green")
                    else:
                        axs[row,col].scatter(XY.x, XY.y, color="red")
                
                axs[row,col].set_ylim(0,1)
                axs[row,col].set_xlim(0,1)
                axs[row,col].set_title("Approximate Value of Pi = " + str(pis[spot]))
                spot += 1
    plt.show()

def rand_coords(radius, dots, rounds):
    XY_rounds = list()

    for _ in range(0,rounds):
        rand_XY = list()
        
        for _ in range(0,dots):
            x = random.uniform(0,radius)
            y = random.uniform(0,radius)
            rand_XY.append(XY(x,y))
        XY_rounds.append(rand_XY)
    
    return XY_rounds

def approximate_pi(XYs, radius):
    PIs = list()
    for xy in XYs:
        in_circle = [c for c in xy if c.in_circle(radius)]
        in_circle_count = len(in_circle)

        PIs.append(4* (in_circle_count/len(xy)))
    return PIs


if __name__ == "__main__":
    args = docopt(__doc__)

    radius = int(args["<radius>"]) if args["<radius>"] is not None else 1
    dots = int(args["<dots>"]) if args["<dots>"] is not None else 100
    rounds = int(args["<rounds>"]) if args["<rounds>"] is not None else 4

    XYs = rand_coords(radius, dots, rounds)
    PIs = approximate_pi(XYs, radius)
    plot_simulation(radius, XYs, PIs)