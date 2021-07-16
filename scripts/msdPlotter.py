#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt

def draw(fileName):
    with open(fileName, 'r') as f:
        jar = f.readlines()
    jar = jar[2:]

    step = []
    bar = []
    for x in jar:
        step.append(float(x.split()[0]))
        bar.append(float(x.split()[9]))

    tag = fileName[fileName.find('.')+1:]
    plt.plot(step, bar, label=tag)

if __name__ == "__main__":
    folder = sys.argv[1:]
    print(folder)
    for file in folder:
        draw(file)

    plt.legend()
    plt.show()
