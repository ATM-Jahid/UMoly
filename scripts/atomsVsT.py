#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt
from statistics import mean, stdev

def main():
    files = sys.argv[1:]
    foo = [[0 for j in range(5)] for i in range(7)]

    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()

        u = int(jar[1].split()[3][:-1])
        mo = int(jar[1].split()[7])
        temp = int(file[file.find('at')+2:file.find('/')])
        num = int(file[-1])
        foo[(temp-600)//100][num-1] = u + mo

    with open('baz.txt', 'a') as f:
        for i in range(7):
            f.write(f'{100 * i + 600}' + ' ')
            for j in range(5):
                f.write(f'{foo[i][j]}' + ' ')
            f.write('\n')

    x = []; y = []; err = []
    for i in range(7):
        x.append(1e4/(100 * i + 600))
        y.append(mean(foo[i]))
        err.append(stdev(foo[i]))

    plt.figure(figsize=(5,4))
    plt.errorbar(x, y, err, ls='-',
            marker='o', ms=3, mfc=plt.cm.viridis(0.9), mec=plt.cm.viridis(0.9),
            capsize=5, color=plt.cm.viridis(0.5), ecolor=plt.cm.viridis(0.75))
    plt.xlabel(r'$10^4$/T (1/K)')
    plt.ylabel('Number of diffusing atoms')
    plt.tight_layout()
    plt.savefig('atomsVsT.pdf')

if __name__ == '__main__':
    main()
