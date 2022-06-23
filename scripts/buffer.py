#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt

def main():
    # input "unwDump" files
    files = sys.argv[1:]
    print(files)

    for file in files:
        extract(file)

    plt.legend()
    plt.show()

def extract(file):
    with open(file, 'r') as f:
        jar = f.readlines()

    fileName = file[file.find('.')+1:]
    sqdiFile = f'sqdi_last.{fileName}'
    writeFile = f'buff_msd.{fileName}'

    N = int(jar[3])
    chunk = N + 9
    timesteps = len(jar) // chunk

    with open(sqdiFile, 'r') as f:
        foo = f.readlines()
    for i in range(len(foo)):
        tmp = foo[i].split()
        foo[i] = [int(tmp[0]), int(float(tmp[1]) > 3)]

    num_bulk_u = 0; num_bulk_mo = 0
    num_gb_u = 0; num_gb_mo = 0
    for line in foo:
        if line[1]:         # bulk
            if line[0] == 1:        # U in bulk
                num_bulk_u += 1
            elif line[0] == 2:      # Mo in bulk
                num_bulk_mo += 1
        else:               # gb
            if line[0] == 1:        # U in gb
                num_gb_u += 1
            elif line[0] == 2:      # Mo in gb
                num_gb_mo += 1
    assert (num_bulk_u+num_bulk_mo+num_gb_u+num_gb_mo) == N

    buffDiff = 5
    buffLen = 50
    bulk_u = [0]*buffLen; bulk_mo = [0]*buffLen
    gb_u_2d = [0]*buffLen; gb_mo_2d = [0]*buffLen
    gb_u_3d = [0]*buffLen; gb_mo_3d = [0]*buffLen

    for b in range(0, timesteps-buffLen, buffDiff):
        r_init = []
        for line in jar[b*chunk+9: (b+1)*chunk]:
            tmp = line.split()
            r_init.append([float(x) for x in tmp[2:]])

        for j in range(buffLen):
            for ii in range(N):
                r_curr = [float(x) for x in jar[(b+j+1)*chunk+9+ii].split()[2:]]
                d2 = (r_curr[0] - r_init[ii][0]) ** 2 + (r_curr[2] - r_init[ii][2]) ** 2
                d3 = d2 + (r_curr[1] - r_init[ii][1]) ** 2
                if foo[ii][1]:          # bulk
                    if foo[ii][0] == 1:         # U in bulk
                        bulk_u[j] += d3
                    elif foo[ii][0] == 2:       # Mo in bulk
                        bulk_mo[j] += d3
                else:                   # gb
                    if foo[ii][0] == 1:         # U in gb
                        gb_u_2d[j] += d2
                        gb_u_3d[j] += d3
                    elif foo[ii][0] == 2:       # Mo in gb
                        gb_mo_2d[j] += d2
                        gb_mo_3d[j] += d3

    numBuff = (len(jar) - buffLen) // buffDiff + 1
    bulk_u = [x / num_bulk_u / numBuff for x in bulk_u]
    bulk_mo = [x / num_bulk_mo / numBuff for x in bulk_mo]
    gb_u_2d = [x / num_gb_u / numBuff for x in gb_u_2d]
    gb_mo_2d = [x / num_gb_mo / numBuff for x in gb_mo_2d]
    gb_u_3d = [x / num_gb_u / numBuff for x in gb_u_3d]
    gb_mo_3d = [x / num_gb_mo / numBuff for x in gb_mo_3d]

    tag = file[file.find('.')+1:]
    plt.plot(gb_u_2d, label=tag)

if __name__ == '__main__':
    main()
