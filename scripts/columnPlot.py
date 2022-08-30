#!/usr/bin/env python

import sys
import itertools
import numpy as np
import matplotlib.pyplot as plt

def draw(file, colus, flags, mark, colo, lstyle):
    with open(file, 'r') as f:
        jar = f.readlines()
    jar = jar[2:]

    x = []; y = []
    colu1 = next(colus)
    for line in jar:
        tmp = line.split()
        x.append(float(tmp[colu1[0]]))
        y.append(float(tmp[colu1[1]]))

    overT = [1e4/T for T in x]
    logD = [np.log(D) for D in y]

    m, b = np.polyfit(overT, logD, 1)
    y_fit = [m*x+b for x in overT]

    colo1 = next(colo)
    tint1 = plt.cm.jet(colo1)
    lstyle1 = next(lstyle)
    mark1 = next(mark)
    tag = next(flags)

    plt.plot(overT, np.exp(y_fit), ls=lstyle1, color=tint1)
    plt.scatter(overT, y, marker=mark1, color=tint1)
    plt.plot([], [], color=tint1, marker=mark1, ls=lstyle1, label=tag)

def main():
    # input files where x and y are in columns
    files = sys.argv[1:]

    n = len(files)
    if n > 1:
        tints = itertools.cycle(tuple([i/(n-1) for i in range(n)]))
    else:
        tints = itertools.cycle((0.3, 0.7))
    markers = itertools.cycle(('o','s','p','v','x','+'))
    lines = itertools.cycle(('-', '--', ':', '-.', (0, (5, 10)), (0, (3, 1, 1, 10))))

    # hardcoded
    columns = itertools.cycle(([0,1], [0,3], [0,5]))
    tags = itertools.cycle(('U', 'Mo', 'Xe'))

    plt.figure(figsize=(5,4))
    for file in files:
        draw(file, columns, tags, markers, tints, lines)

    #plt.ylim(1e-14, 1e-10)
    plt.xlabel(r'$10^4$/T (1/K)')
    plt.ylabel(r'Diffusivity (m$^2$s$^{-1}$)')
    plt.yscale('log')
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
