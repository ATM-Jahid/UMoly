#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt

def draw(file):
    with open(file, 'r') as f:
        jar = f.readlines()
    jar = jar[2:]

    x = []; y_xe = []; e_xe = []
    for line in jar:
        tmp = line.split()
        x.append(float(tmp[0]))
        y_xe.append(float(tmp[1]))
        e_xe.append(float(tmp[2]))

    overT = [1/T for T in x]
    plt.errorbar(overT, y_xe, e_xe, label='Xe')
    plt.yscale('log')
    plt.legend()
    plt.show()

def main():
    # input "xe_diff" files
    files = sys.argv[1:]
    for file in files:
        draw(file)

if __name__ == '__main__':
    main()
