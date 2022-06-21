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
        chkMsdFile = f'check_msd.{fileName}'
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

        # define a previous timestep for periodicity considerations
        r_prev = copy.deepcopy(r_init)

        # loop over all timesteps
        r_curr = [0]*(N+1)
        fooPrint = ''
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

                    pos = (r_curr[ii][l+4] + r_curr[ii][l+1]) * (bhi[l] - blo[l])
                    atom_unw[ii][l+1] = pos

            # print atom MSDs to a file
            with open(atomUnwFile, 'a') as f:
                f.write(f'ITEM: TIMESTEP\n{timestep}\n' +
                        f'ITEM: NUMBER OF ATOMS\n{N}\n' +
                        f'ITEM: BOX BOUNDS pp pp pp\n' +
                        f'{blo[0]} {bhi[0]}\n{blo[1]} {bhi[1]}\n{blo[2]} {bhi[2]}\n' +
                        f'ITEM: ATOMS id type xu yu zu\n')
                for x in range(1, len(atom_unw)):
                    f.write(f'{x} {atom_unw[x][0]} {atom_unw[x][1]:.5} '
                        + f'{atom_unw[x][2]:.5} {atom_unw[x][3]:.5}\n')

            # prep for next iteration
            r_prev = copy.deepcopy(r_curr)

if __name__ == '__main__':
    main()
