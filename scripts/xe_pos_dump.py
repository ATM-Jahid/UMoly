#!/usr/bin/env python3

import sys
import copy

def main():
    # input "dumpRun" files
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
    timesteps = len(jar) // chunk

    # boundary values
    blo, bhi = [[0]*3, [0]*3]
    for i in range(3):
        blo[i], bhi[i] = [float(x) for x in jar[5+i].split()]

    # initalize xe pos
    xe_init = {}
    xe_unw = {}
    for line in jar[9: chunk]:
        tmp = line.split()
        if int(tmp[1]) == 3:
            xe_init[tmp[0]] = []
            xe_unw[tmp[0]] = []
            for l in range(3):
                xe_init[tmp[0]].append(float(tmp[2+l]))
                xe_unw[tmp[0]].append(bhi[l] * (2 * xe_init[tmp[0]][l] - 1))
            xe_init[tmp[0]].extend([0,0,0])
            # break after you find 2 Xe atoms
            if len(xe_init) == 2:
                break

    # use dumper
    dumper(xePosFile, 0, blo, bhi, xe_unw)

    # define a previous timestep for PBC
    xe_prev = copy.deepcopy(xe_init)

    # loop over timesteps
    for i in range(1, timesteps):
        timestep = int(jar[i*chunk+1])
        xe_curr = {}
        # go through lines of a timestep
        for line in jar[i*chunk+9: (i+1)*chunk]:
            tmp = line.split()
            if int(tmp[1]) == 3:
                xe_curr[tmp[0]] = [0]*6
                for l in range(3):
                    # PBC
                    xe_curr[tmp[0]][l] = float(tmp[2+l])
                    if xe_prev[tmp[0]][l] > 0.75 and xe_curr[tmp[0]][l] < 0.25:
                        xe_curr[tmp[0]][l+3] = xe_prev[tmp[0]][l+3] + 1
                    elif xe_prev[tmp[0]][l] < 0.25 and xe_curr[tmp[0]][l] > 0.75:
                        xe_curr[tmp[0]][l+3] = xe_prev[tmp[0]][l+3] - 1
                    else:
                        xe_curr[tmp[0]][l+3] = xe_prev[tmp[0]][l+3]

                    # scaled value
                    xe_unw[tmp[0]][l] = bhi[l] * \
                            (2 * (xe_curr[tmp[0]][l] + xe_curr[tmp[0]][l+3]) - 1)

                if len(xe_curr) == 2:
                    break

        # use dumper
        dumper(xePosFile, timestep, blo, bhi, xe_unw)

        # prep for next iteration
        xe_prev = copy.deepcopy(xe_curr)

def dumper(writeFile, time, loB, upB, unw):
    with open(writeFile, 'a') as f:
        f.write(f'ITEM: TIMESTEP\n{time}\n' +
                'ITEM: NUMBER OF ATOMS\n2\n' +
                f'ITEM: BOX BOUNDS pp pp pp\n' +
                f'{loB[0]} {upB[0]}\n{loB[1]} {upB[1]}\n{loB[2]} {upB[2]}\n' +
                f'ITEM: ATOMS id type xu yu zu\n')
        # sort the unw
        for k, v in dict(sorted(unw.items())).items():
            f.write(f'{k} 3 {v[0]:.5} {v[1]:.5} {v[2]:.5}\n')

if __name__ == '__main__':
    main()
