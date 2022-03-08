#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt

def main():
    files = sys.argv[1:]
    print(files)

    diffs_gb = []
    diffs_bulk = []
    diff_atoms = []

    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()

        jar = [float(x) for x in jar]
        foo = []
        bar = []
        for x in jar:
            if x > 3:
                foo.append(x)
            else:
                bar.append(x)

        diff_atoms.append(len(foo))
        diffs_gb.append(sum(foo)/len(foo))
        diffs_bulk.append(sum(bar)/len(bar))

    print(diff_atoms)
    print(diffs_gb)
    print(diffs_bulk)

    diffs_gb = [x/40*1e-11 for x in diffs_gb]
    diffs_bulk = [x/40*1e-11 for x in diffs_bulk]
    temps = list(range(600, 1300, 100))
    temps = [1/x for x in temps]

    plt.plot(temps, diffs_gb)
    plt.scatter(temps, diffs_gb, c='r')
    #plt.plot(temps, diffs_bulk)
    plt.yscale('log')
    #plt.scatter(temps, diff_atoms, c='r')
    #plt.plot(temps, diff_atoms)
    #for i, j in zip(temps, diff_atoms):
    #    plt.text(i, j+50, f'{j}')
    plt.show()

if __name__ == '__main__':
    main()
