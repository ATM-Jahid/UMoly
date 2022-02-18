#!/usr/bin/env python3

import sys
import copy

def main():
    files = sys.argv[1:]
    print(files)

    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()

        # number of atoms
        N = int(jar[3])
        chunk = N + 9

        # boundary values
        blo, bhi = [[0]*3, [0]*3]
        for i in range(3):
            blo[i], bhi[i] = [float(x) for x in jar[5*chunk+5+i].split()]

        # initialize atom positions
        r_init = [0]*(N+1)
        for line in jar[5*chunk+9: 6*chunk]:
            # store line values temporarily
            tmp = line.split()
            ii = int(tmp[0])
            r_init[ii] = [int(tmp[1])]
            for i in tmp[2:]:
                r_init[ii].append(float(i))
            # add more entries for periodic considerations
            r_init[ii].extend([0,0,0])

        # define a previous timestep for periodicity considerations
        r_prev = copy.deepcopy(r_init)

        # loop over all timesteps
        r_curr = [0]*(N+1)
        dr = [0]*3
        for i in range(6, 106):
            # initialize MSD variable
            Nmsd = 0
            # go through the lines of a timestep
            for line in jar[i*chunk+9: (i+1)*chunk]:
                tmp = line.split()
                ii = int(tmp[0])
                r_curr[ii] = [int(tmp[1])]
                for j in tmp[2:]:
                    r_curr[ii].append(float(j))
                # don't forget to copy the values from prev timestep later
                r_curr[ii].extend([0,0,0])

                # put boundary jump counters here
                for l in range(3):
                    cutoff = 0.75
                    if r_prev[ii][l+1] > cutoff and r_curr[ii][l+1] < (1-cutoff):
                        r_curr[ii][l+4] = r_prev[ii][l+4] + 1
                    elif r_prev[ii][l+1] < (1-cutoff) and r_curr[ii][l+1] > cutoff:
                        r_curr[ii][l+4] = r_prev[ii][l+4] - 1
                    else:
                        r_curr[ii][l+4] = r_prev[ii][l+4]

                    dspl = r_curr[ii][l+4] + r_curr[ii][l+1] - r_init[ii][l+1]
                    dr[l] = dspl * (bhi[l] - blo[l])
                    Nmsd += dr[l] * dr[l]
            msd = Nmsd / N
            print(msd)

            # print out the MSDs in a file
            with open('fakedump', 'a') as f:
                f.write(str((i-5)*50000) + '\t' + str(msd) + '\n')

            # prep for next iteration
            r_prev = copy.deepcopy(r_curr)

        atom_msd = [0]*(N+1)
        for ii in range(1, N+1):
            jj = 0
            for l in range(3):
                dspl = r_curr[ii][l+4] + r_curr[ii][l+1] - r_init[ii][l+1]
                d = dspl * (bhi[l] - blo[l])
                jj += d * d
            atom_msd[ii] = jj

        with open('atom_msd.txt', 'a') as f:
            for line in atom_msd:
                f.write(str(line) + '\n')

if __name__ == '__main__':
    main()
