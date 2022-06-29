#!/usr/bin/env python3

import sys

def main():
    # input "unwDump" files
    files = sys.argv[1:]
    print(files)

    for file in files:
        extract(file)

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
        foo[i] = [int(tmp[0]), float(tmp[1]) < 3]

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

    buffDiff = 10
    buffLen = 50
    bulk_u = [0]*buffLen; bulk_mo = [0]*buffLen
    gb_u_2d = [0]*buffLen; gb_mo_2d = [0]*buffLen
    gb_u_3d = [0]*buffLen; gb_mo_3d = [0]*buffLen

    start = 20
    for b in range(start, timesteps-buffLen, buffDiff):
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

    numBuff = (timesteps - buffLen - start) // buffDiff + 1
    # avoid "div by zero" error
    if num_bulk_u:
        bulk_u = [x / num_bulk_u / numBuff for x in bulk_u]
    if num_gb_u:
        gb_u_2d = [x / num_gb_u / numBuff for x in gb_u_2d]
        gb_u_3d = [x / num_gb_u / numBuff for x in gb_u_3d]
    if num_bulk_mo:
        bulk_mo = [x / num_bulk_mo / numBuff for x in bulk_mo]
    if num_gb_mo:
        gb_mo_2d = [x / num_gb_mo / numBuff for x in gb_mo_2d]
        gb_mo_3d = [x / num_gb_mo / numBuff for x in gb_mo_3d]

    with open(writeFile, 'a') as f:
        f.write(f'#Number of buffers: {numBuff}\n' +
                f'#U in gb: {num_gb_u}; #Mo in gb: {num_gb_mo}\n' +
                f'#U in bulk: {num_bulk_u}; #Mo in bulk: {num_bulk_mo}\n' +
                '#Buffer averaged mean squared displacements\n' +
                '#gb_u_2d gb_mo_2d gb_u_3d gb_mo_3d bulk_u bulk_mo\n' +
                '0 0 0 0 0 0\n')
        for i in range(buffLen):
            f.write(f'{gb_u_2d[i]:.5} {gb_mo_2d[i]:.5} ' +
                    f'{gb_u_3d[i]:.5} {gb_mo_3d[i]:.5} ' +
                    f'{bulk_u[i]:.5} {bulk_mo[i]:.5}\n')

if __name__ == '__main__':
    main()
