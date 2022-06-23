#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt

def main():
    files = sys.argv[1:]
    print(files)

    for file in files:
        extract(file)

    plt.legend()
    plt.show()

def extract(file):
    with open(file, 'r') as f:
        jar = f.readlines()

    buffDiff = 5
    buffLen = 50
    msd = [0]*buffLen
    for b in range(0, len(jar)-buffLen, buffDiff):
        xe_init = [float(x) for x in jar[b].split()]
        for i in range(buffLen):
            xe_curr = [float(x) for x in jar[b+i+1].split()]
            d = 0
            for l in range(3):
                d += (xe_curr[l] - xe_init[l]) ** 2
            msd[i] += d

    numBuff = (len(jar) - buffLen) // buffDiff + 1
    msd = [x / numBuff for x in msd]
    tag = file[file.find('.')+1:]
    plt.plot(msd, label=tag)

if __name__ == '__main__':
    main()
