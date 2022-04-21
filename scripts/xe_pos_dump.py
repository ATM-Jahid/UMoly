#!/usr/bin/env python3

import sys
import copy

def main():
    files = sys.argv[1:]
    print(files)

    for file in files:
        extract(file)

def extract(file):
    # make a write file
    fileName = file[file.find('.')+1:]
    xePosFile = f'xe_pos.{fileName}'

    with open(file, 'r') as f:
        jar = f.readlines()

    # number of atoms
    N = int(jar[3])
    chunk = N + 9

    # boundary values
    blo, bhi = [[0]*3, [0]*3]
    for i in range(3):
        blo[i], bhi[i] = [float(x) for x in jar[5+i].split()]

    # initalize xe pos
    xe_init = [0]*6
    foo = ''
    for line in jar[9: chunk]:
        tmp = line.split()
        if int(tmp[1]) == 3:
            for l in range(3):
                xe_init[l] = float(tmp[2+l])
                sc = bhi[l] * (2 * xe_init[l] - 1)
                foo += str(sc) + ' '
            foo = foo[:-1] + '\n'
            break

    with open(xePosFile, 'w') as f:
        f.write(foo)

    # define a previous timestep for PBC
    xe_prev = copy.deepcopy(xe_init)

    # loop over timesteps
    xe_curr = [0]*6
    foo = ''
    for i in range(1, 401):
        # go through lines of a timestep
        for line in jar[i*chunk+9: (i+1)*chunk]:
            tmp = line.split()
            if int(tmp[1]) == 3:
                for l in range(3):
                    # PBC
                    xe_curr[l] = float(tmp[2+l])
                    if xe_prev[l] > 0.75 and xe_curr[l] < 0.25:
                        xe_curr[l+3] = xe_prev[l+3] + 1
                    elif xe_prev[l] < 0.25 and xe_curr[l] > 0.75:
                        xe_curr[l+3] = xe_prev[l+3] - 1
                    else:
                        xe_curr[l+3] = xe_prev[l+3]

                    # scaled value
                    sc = bhi[l] * (2 * (xe_curr[l] + xe_curr[l+3]) - 1)
                    foo += str(sc) + ' '
                foo = foo[:-1] + '\n'
                xe_prev = copy.deepcopy(xe_curr)
                break

    with open(xePosFile, 'a') as f:
        f.write(foo)

if __name__ == '__main__':
    main()
