#!/usr/bin/env python3

import sys
import statistics
import numpy as np
import matplotlib.pyplot as plt

slopes = []

def draw(fileName):
    with open(fileName, 'r') as f:
        jar = f.readlines()
    jar = jar[11:]

    step = []
    bar = []

    for x in jar:
        step.append(float(x.split()[0]))
        bar.append(float(x.split()[9]))

    m, b = np.polyfit(step, bar, 1)
    print(m, '\t', b)
    slopes.append(m)

    ordinate = [m*x+b for x in step]

    tag = fileName[fileName.find('.')+1:]
    plt.plot(step, ordinate, label=tag)

def stat(slopeJar):
    print("Mean: ", statistics.mean(slopeJar))
    print("Stdev: ", statistics.stdev(slopeJar))

if __name__ == "__main__":
    folder = sys.argv[1:]
    print(folder)
    for file in folder:
        draw(file)

    stat(slopes)

    plt.legend()
    plt.show()
