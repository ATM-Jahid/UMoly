#!/usr/bin/env python3

import sys
import itertools
import numpy as np
import matplotlib.pyplot as plt

def draw(file, mark, colo, lstyle):
    with open(file, 'r') as f:
        jar = f.readlines()
    jar = jar[2:]
    fileName = file[file.find('s.')+2:]

    x = []
    y_tot = []; e_tot = []
    for line in jar:
        tmp = line.split()
        x.append(float(tmp[0]))
        y_tot.append(float(tmp[5]))
        e_tot.append(float(tmp[6]))

    overT = [1e4/T for T in x]
    logD_tot = [np.log(D) for D in y_tot]

    m1, b1 = np.polyfit(overT, logD_tot, 1)
    u_fit = [m1*x+b1 for x in overT]

    colo1 = next(colo)
    tint1 = plt.cm.jet(colo1)
    lstyle1 = next(lstyle)
    mark1 = next(mark)
    tag = f"{fileName.split('_')[0]} {{{fileName.split('_')[1]}}}"
    #tag = f"{fileName[fileName.find('/')+1:fileName.find('.')]}"

    plt.plot(overT, np.exp(u_fit), ls=lstyle1, color=tint1)
    plt.scatter(overT, y_tot, marker=mark1, color=tint1)
    plt.plot([], [], color=tint1, marker=mark1, ls=lstyle1, label=tag)

def main():
    # input "diffusivities" files of compositions
    files = sys.argv[1:]

    n = len(files)
    tints = itertools.cycle(tuple([i/(n-1) for i in range(n)]))
    markers = itertools.cycle(('o','s','p','v','x','+'))
    lines = itertools.cycle(('-', '--', ':', '-.', (0, (5, 10)), (0, (3, 1, 1, 10))))

    plt.figure(figsize=(5,4))
    for file in files:
        draw(file, markers, tints, lines)

    plt.ylim(1e-13, 1e-10)
    plt.xlabel(r'$10^4$/T (1/K)')
    plt.ylabel(r'Diffusivity (m$^2$s$^{-1}$)')
    plt.yscale('log')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{files[0][:files[0].find('/')]}.pdf")
    #plt.savefig('composition.pdf')
    plt.show()

if __name__ == '__main__':
    main()
