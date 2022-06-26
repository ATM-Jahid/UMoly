#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean, stdev

def draw(fileName, writeFile, p):
    with open(fileName, 'r') as f:
        jar = f.readlines()
    jar = jar[5:]

    u = []; mo = []
    for line in jar:
        tmp = line.split()
        u.append(float(tmp[0]))
        mo.append(float(tmp[1]))
    step = list(range(len(u)))

    m1, b1 = np.polyfit(step, u, 1)
    m2, b2 = np.polyfit(step, mo, 1)

    with open(writeFile, 'a') as f:
        f.write(f'U: {m1:0.6} {b1:0.6}\nMo: {m2:0.6} {b2:0.6}\n')

    if p:
        ordinate1 = [m1*x+b1 for x in step]
        ordinate2 = [m2*x+b2 for x in step]

        plt.plot(step, u, 'r--', label='U')
        plt.plot(step, ordinate1, 'r')
        plt.plot(step, mo, 'g--', label='Mo')
        plt.plot(step, ordinate2, 'g')
        plt.legend()
        plt.show()

def main():
    folder = sys.argv[1:]
    if '-p' in folder:
        folder.remove('-p')
        p = 1
    else:
        p = 0
    print(folder)

    file1 = folder[0]
    fileName = file1[file1.find('.')+1:-2]
    writeFile = f'clf_slopes.{fileName}'

    with open(writeFile, 'a') as f:
        f.write('# Slopes for diffusing atom MSDs\n' +
                '# Type: Slope Intercept\n')

    for file in folder:
        draw(file, writeFile, p)

if __name__ == "__main__":
    main()
