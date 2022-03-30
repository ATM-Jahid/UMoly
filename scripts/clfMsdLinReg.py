#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean, stdev

def draw(fileName, writeFile):
    with open(fileName, 'r') as f:
        jar = f.readlines()
    jar = jar[11:]

    step = []; tot = []
    x = []; y = []; z = []

    for line in jar:
        tmp = line.split()
        step.append(float(tmp[0]))
        x.append(float(tmp[1]))
        y.append(float(tmp[2]))
        z.append(float(tmp[3]))
        tot.append(float(tmp[4]))

    m1, b1 = np.polyfit(step, x, 1)
    m2, b2 = np.polyfit(step, y, 1)
    m3, b3 = np.polyfit(step, z, 1)
    m4, b4 = np.polyfit(step, tot, 1)

    with open(writeFile, 'a') as f:
        f.write(f'{m1:0.6}\t{m2:0.6}\t{m3:0.6}\t{m4:0.6}\n')

    ordinate1 = [m1*x+b1 for x in step]
    ordinate2 = [m2*x+b2 for x in step]
    ordinate3 = [m3*x+b3 for x in step]
    ordinate4 = [m4*x+b4 for x in step]

    plt.plot(step, ordinate1, 'r')
    plt.plot(step, ordinate2, 'g')
    plt.plot(step, ordinate3, 'b')
    plt.plot(step, ordinate4, 'k')
    plt.show()

def main():
    folder = sys.argv[1:]
    print(folder)

    file1 = folder[0]
    fileName = file1[file1.find('.')+1:-2]
    writeFile = f'clf_slopes.{fileName}'

    with open(writeFile, 'a') as f:
        f.write('# Slopes for diffusing atom MSDs\n')
        f.write('# x y z r\n')

    for file in folder:
        draw(file, writeFile)

if __name__ == "__main__":
    main()
