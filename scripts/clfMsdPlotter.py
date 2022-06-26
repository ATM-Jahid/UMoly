#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt

def main():
    # input "buff_msd" files
    files = sys.argv[1:]
    print(files)

    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()
        jar = jar[5:]

        u = []; mo = []
        for line in jar:
            tmp = line.split()
            u.append(float(tmp[0]))
            mo.append(float(tmp[1]))

        plt.plot(u, 'r', label='U')
        plt.plot(mo, 'g', label='Mo')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    main()
