#!/usr/bin/env python3

import sys
import copy

def main():
    files = sys.argv[1:]
    print(files)

    # input "dumpRun" files
    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()

        # make write files for unwrapped dump
        fileName = file[file.find('.')+1:]
        atomUnwFile = f'unwDump.{fileName}'

        # number of atoms is constant in dumpRun
        N = int(jar[3])
        chunk = N + 9

        # boundary values are constant since it's an NVT-ensemble
        blo, bhi = [[0]*3, [0]*3]
        for i in range(3):
            blo[i], bhi[i] = [float(x) for x in jar[5*chunk+5+i].split()]

        # initialize atom positions
        r_init = [0]*(N+1)
        atom_unw = [[0 for i in range(4)] for j in range(N+1)]
        for line in jar[9: chunk]:
            # store line values temporarily
            tmp = line.split()
            ii = int(tmp[0])
            r_init[ii] = [int(tmp[1])]
            atom_unw[ii][0] = int(tmp[1])
            for i in tmp[2:]:
                r_init[ii].append(float(i))
            # add more entries for periodic considerations
            r_init[ii].extend([0,0,0])

            for l in range(3):
                scaled = r_init[ii][l+1] * (bhi[l] - blo[l])
                atom_unw[ii][l+1] = scaled - bhi[l]

        # print timestep 0
        dumper(atomUnwFile, 0, N, blo, bhi, atom_unw)

        # define a previous timestep for periodicity considerations
        r_prev = copy.deepcopy(r_init)

        # loop over all timesteps
        r_curr = [0]*(N+1)
        for i in range(1, 101):
            # get timestep
            timestep = int(jar[i*chunk+1])
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
                        # not copying values from previous timestep introduced a bug
                        r_curr[ii][l+4] = r_prev[ii][l+4]

                    scaled = (r_curr[ii][l+4] + r_curr[ii][l+1]) * (bhi[l] - blo[l])
                    atom_unw[ii][l+1] = scaled - bhi[l]

            # print into unwDump file
            dumper(atomUnwFile, timestep, N, blo, bhi, atom_unw)

            # prep for next iteration
            r_prev = copy.deepcopy(r_curr)

def dumper(writeFile, time, num_atom, loB, upB, unw_jar):
    with open(writeFile, 'a') as f:
        f.write(f'ITEM: TIMESTEP\n{time}\n' +
                f'ITEM: NUMBER OF ATOMS\n{num_atom}\n' +
                f'ITEM: BOX BOUNDS pp pp pp\n' +
                f'{loB[0]} {upB[0]}\n{loB[1]} {upB[1]}\n{loB[2]} {upB[2]}\n' +
                f'ITEM: ATOMS id type xu yu zu\n')
        for x in range(1, len(unw_jar)):
            f.write(f'{x} {unw_jar[x][0]} {unw_jar[x][1]:.5} '
                + f'{unw_jar[x][2]:.5} {unw_jar[x][3]:.5}\n')

if __name__ == '__main__':
    main()
