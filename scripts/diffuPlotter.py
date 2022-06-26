#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt

def draw(file):
    with open(file, 'r') as f:
        jar = f.readlines()
    jar = jar[2:]

    x = []; y_u = []; e_u = []
    y_mo = []; e_mo = []
    for line in jar:
        tmp = line.split()
        x.append(float(tmp[0]))
        y_u.append(float(tmp[1]))
        e_u.append(float(tmp[2]))
        y_mo.append(float(tmp[3]))
        e_mo.append(float(tmp[4]))

    overT = [1/T for T in x]
    plt.errorbar(overT, y_u, e_u, c='r', label='U')
    plt.errorbar(overT, y_mo, e_mo, c='g', label='Mo')
    plt.yscale('log')
    plt.legend()
    plt.show()

def main():
    # input "diffusivities" files
    files = sys.argv[1:]
    for file in files:
        draw(file)

if __name__ == '__main__':
    main()
