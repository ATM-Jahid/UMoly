#!/usr/bin/env python3

import sys
import copy
import numpy as np
import matplotlib.pyplot as plt

files = sys.argv[1:]
print(files)

for file in files:
    with open(file, 'r') as f:
        jar = f.readlines()

    # number of atoms
    N = int(jar[3])

    # boundary values
    blo, bhi = [[0]*3, [0]*3]
    for i in range(3):
        blo[i], bhi[i] = [float(x) for x in jar[5*(N+9)+5+i].split()]

    # initialize atom positions
    r_init = [0]*(N+1)
    for line in jar[5*(N+9)+9: 6*(N+9)]:
        # store line values temporarily
        tmp = line.split()
        ii = int(tmp[0])
        r_init[ii] = [int(tmp[1])]
        for i in tmp[2:]:
            r_init[ii].append(float(i))
        # add more entries for periodic considerations
        r_init[ii].extend([0,0,0])

    # define a previous timestep for periodicity considerations
    #r_prev = copy.deepcopy(r_init)

    # loop over all timesteps
    r_curr = [0]*(N+1)
    dr = [0]*3
    for i in range(6, 106):
        # calculate MSD for each timestep
        Nmsd = 0
        # go through lines of a timestep
        for line in jar[i*(N+9)+9: (i+1)*(N+9)]:
            tmp = line.split()
            ii = int(tmp[0])
            r_curr[ii] = [int(tmp[1])]
            for j in tmp[2:]:
                r_curr[ii].append(float(j))
            r_curr[ii].extend([0,0,0])

            # put boundary jump counters here
            for l in range(3):
                if r_init[ii][l+1] > 0.9 and r_curr[ii][l+1] < 0.1:
                    r_curr[ii][l+4] = r_init[ii][l+4] + 1
                    #print(r_curr[ii][l+1], r_init[ii][l+1])
                elif r_init[ii][l+1] < 0.1 and r_curr[ii][l+1] > 0.9:
                    r_curr[ii][l+4] = r_init[ii][l+4] - 1
                    #print(r_curr[ii][l+1], r_init[ii][l+1])

            # calculate dx, dy and dz
            for k in range(3):
                r_dspl = r_curr[ii][k+4] + r_curr[ii][k+1]
                dr[k] = (r_dspl - r_init[ii][k+1]) * (bhi[k] - blo[k])
                #print(f'dr of {k}: {dr[k]}')
                Nmsd += dr[k] * dr[k]
        msd = Nmsd / N
        print(msd)

        # print out the MSDs in a file
        with open('fakedump', 'a') as f:
            f.write(str((i-5)*50000) + '\t' + str(msd) + '\n')

        # prep for next iteration
        #r_prev = copy.deepcopy(r_curr)
