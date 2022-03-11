#!/usr/bin/env python3

import sys
import copy

def main():
    files = sys.argv[1:]
    print(files)

    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()

        # make a write file
        fileName = file[file.find('.')+1:]
        avgMsdFile = f'check_avg_msd.{fileName}'
        atomMsdFile = f'atom_msd_dump.{fileName}'

        # number of atoms
        N = int(jar[3])
        chunk = N + 9

        # boundary values
        blo, bhi = [[0]*3, [0]*3]
        for i in range(3):
            blo[i], bhi[i] = [float(x) for x in jar[5*chunk+5+i].split()]

        # initialize atom positions
        r_init = [0]*(N+1)
        atom_msd = [[0 for i in range(4)] for j in range(N+1)]
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
        fooPrint = ''
        for i in range(6, 106):
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
                        r_curr[ii][l+4] = r_prev[ii][l+4]

                    dspl = r_curr[ii][l+4] + r_curr[ii][l+1] - r_init[ii][l+1]
                    d = dspl * (bhi[l] - blo[l])
                    atom_msd[ii][l] = d * d

                # add all the components
                atom_msd[ii][3] = atom_msd[ii][0] + atom_msd[ii][1] + atom_msd[ii][2]
                Nmsd += atom_msd[ii][3]

            # calculate and add MSDs to a string
            msd = Nmsd / N
            print(msd)
            fooPrint += str(timestep) + '\t' + str(msd) + '\n'

            # print atom MSDs to a file
            with open(atomMsdFile, 'a') as f:
                f.write(f'TIMESTEP: {timestep}' + '\n')
                f.write('x^2' + '\t' +  'y^2' + '\t' + 'z^2' + '\t' + 'r^2' + '\n')
                for x in range(1, len(atom_msd)):
                    f.write(f'{atom_msd[x][0]:.5}\t{atom_msd[x][1]:.5}\t'
                        + f'{atom_msd[x][2]:.5}\t{atom_msd[x][3]:.7}\n')

            # prep for next iteration
            r_prev = copy.deepcopy(r_curr)

        # print out the total MSDs in a file
        with open(avgMsdFile, 'a') as f:
            f.write(fooPrint)

if __name__ == '__main__':
    main()
