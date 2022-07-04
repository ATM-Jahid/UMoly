#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean, stdev

def draw(fileName, writeFile, p):
    with open(fileName, 'r') as f:
        jar = f.readlines()
    jar = jar[5:]

    xe = []
    for line in jar:
        tmp = line.split()
        xe.append(float(tmp[0]))

    step = list(range(len(xe)))
    m1, b1 = np.polyfit(step, xe, 1)

    with open(writeFile, 'a') as f:
        f.write(f'Xe: {m1:e} {b1:e}\n')

    if p:
        ordinate1 = [m1*x+b1 for x in step]

        plt.plot(step, xe, label='Xe')
        plt.plot(step, ordinate1)
        plt.legend()
        plt.show()

def main():
    # input "xe_msd" files
    folder = sys.argv[1:]
    if '-p' in folder:
        folder.remove('-p')
        p = 1
    else:
        p = 0
    print(folder)

    file1 = folder[0]
    fileName = file1[file1.find('.')+1:-2]
    writeFile = f'xe_slopes.{fileName}'

    with open(writeFile, 'a') as f:
        f.write('# Slopes for Xe MSDs\n' +
                '# Type: Slope Intercept\n')

    for file in folder:
        draw(file, writeFile, p)

if __name__ == "__main__":
    main()
