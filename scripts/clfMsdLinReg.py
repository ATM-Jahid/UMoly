#!/usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt

def draw(fileName, writeFile, p):
    with open(fileName, 'r') as f:
        jar = f.readlines()

    # get number of specific atoms from buff_msd
    # the indices below are hardcoded
    num_u = int(jar[1].split()[3][:-1])
    num_mo = int(jar[1].split()[7])
    jar = jar[5:]

    u = []; mo = []
    for line in jar:
        tmp = line.split()
        u.append(float(tmp[0]))
        mo.append(float(tmp[1]))
    step = list(range(len(u)))
    tot = [(num_u * x + num_mo * y) / (num_u + num_mo)
            for x, y in zip(u, mo)]

    m1, b1 = np.polyfit(step, u, 1)
    m2, b2 = np.polyfit(step, mo, 1)
    m3, b3 = np.polyfit(step, tot, 1)

    with open(writeFile, 'a') as f:
        f.write(f'U: {m1:e} {b1:e}\n' +
                f'Mo: {m2:e} {b2:e}\n' +
                f'Tot: {m3:e} {b3:e}\n')

    if p:
        ordinate1 = [m1*x+b1 for x in step]
        ordinate2 = [m2*x+b2 for x in step]
        ordinate3 = [m3*x+b3 for x in step]

        plt.plot(step, u, 'r--', label='U')
        plt.plot(step, ordinate1, 'r')
        plt.plot(step, mo, 'g--', label='Mo')
        plt.plot(step, ordinate2, 'g')
        plt.plot(step, tot, 'b-.', label='Tot')
        plt.plot(step, ordinate3, 'b')
        plt.legend()
        plt.show()

def main():
    # input "buff_msd" files
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
