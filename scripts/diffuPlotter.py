#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt

def draw(file):
    with open(file, 'r') as f:
        jar = f.readlines()
    jar = jar[2:]

    x = []; y = []; e = []
    for line in jar:
        tmp = line.split()
        x.append(float(tmp[0]))
        y.append(float(tmp[2]))
        e.append(float(tmp[3]))

    overT = [1/T for T in x]
    plt.errorbar(overT, y, e)
    plt.yscale('log')
    plt.show()

def main():
    files = sys.argv[1:]
    for file in files:
        draw(file)

if __name__ == '__main__':
    main()
