#!/usr/bin/env python3

import sys
import copy

def main():
    files = sys.argv[1:]
    print(files)

    # input "unwDump" files
    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()

        # make a write file
        fileName = file[file.find('.')+1:]
        chkMsdFile = f'check_msd.{fileName}'

        # number of atoms
        N = int(jar[3])
        chunk = N + 9
        timesteps = len(jar) // chunk

        # initialize atom positions
        r_init = [0]*(N+1)
        for line in jar[9: chunk]:
            # store line values temporarily
            tmp = line.split()
            ii = int(tmp[0])
            r_init[ii] = [int(tmp[1])]
            for i in tmp[2:]:
                r_init[ii].append(float(i))

        # define a previous timestep for periodicity considerations
        r_prev = copy.deepcopy(r_init)

        # loop over all timesteps
        r_curr = [0]*(N+1)
        fooPrint = ''
        for i in range(1, timesteps):
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

                # put boundary jump counters here
                for l in range(3):
                    d = r_curr[ii][l+1] - r_init[ii][l+1]
                    Nmsd += d * d

            # calculate and add MSDs to a string
            msd = Nmsd / N
            fooPrint += str(timestep) + '\t' + str(msd) + '\n'

            # prep for next iteration
            r_prev = copy.deepcopy(r_curr)

        # print out the total MSDs in a file
        with open(chkMsdFile, 'a') as f:
            f.write(fooPrint)

if __name__ == '__main__':
    main()
