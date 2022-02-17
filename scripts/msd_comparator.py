#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt

def main():
    files = sys.argv[1:]
    print(files)

    with open(files[0], 'r') as f:
        jar_1 = f.readlines()
    jar_1 = jar_1[2:]

    step_1 = []
    bar_1 = []
    for x in jar_1:
        step_1.append(float(x.split()[0]))
        bar_1.append(float(x.split()[9]))

    plt.scatter(step_1, bar_1)
    plt.plot(step_1, bar_1, label='LAMMPS MSD')

    with open(files[1], 'r') as f:
        jar_2 = f.readlines()

    step_2 = []
    bar_2 = []
    for x in jar_2:
        step_2.append(float(x.split()[0]))
        bar_2.append(float(x.split()[1]))

    plt.plot(step_2, bar_2, label='My MSD')

    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
