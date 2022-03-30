#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt

def main():
    files = sys.argv[1:]
    print(files)

    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()
        jar = jar[2:]

        time = []; tot = []
        x = []; y = []; z = []

        for line in jar:
            tmp = line.split()
            time.append(float(tmp[0]))
            x.append(float(tmp[1]))
            y.append(float(tmp[2]))
            z.append(float(tmp[3]))
            tot.append(float(tmp[4]))

        plt.plot(time, x, 'r')
        plt.plot(time, y, 'g')
        plt.plot(time, z, 'b')
        plt.plot(time, tot, 'k')
        plt.show()

if __name__ == '__main__':
    main()
