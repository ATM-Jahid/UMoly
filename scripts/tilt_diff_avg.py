#!/usr/bin/env python

import sys
import numpy as np

def main():
    num_temp = 7
    num_var = 7
    foo = [[0 for j in range(num_var)] for i in range(num_temp)]

    files = sys.argv[1:]
    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()
        jar = jar[2:]

        for i in range(num_temp):
            tmp = jar[i].split()
            for j in range(num_var):
                if j in [0, 1, 3, 5]:
                    foo[i][j] += float(tmp[j])
                else:
                    foo[i][j] += (float(tmp[j]))**2

    N = len(files)
    for i in range(num_temp):
        for j in range(num_var):
            foo[i][j] /= N
        for k in [2, 4, 6]:
            foo[i][k] = np.sqrt(foo[i][k])

    # input "diffusivities" files from the ../ directory
    writeFile = f"{files[0][:files[0].find('/')]}.avg"
    with open(writeFile, 'a') as f:
        f.write('# Tilt-averaged diffusivity\n' +
                '# temp U_mean U_stdev Mo_mean Mo_stdev Tot_mean Tot_stdev\n')
        for i in range(num_temp):
            for j in range(num_var):
                f.write(f'{foo[i][j]:e} ')
            f.write('\n')

if __name__ == '__main__':
    main()
