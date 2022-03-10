#!/usr/bin/env python3

import sys

def main():
    files = sys.argv[1:]
    print(files)

    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()

        # make a write file
        fileName = file[file.find('.')+1:]
        writeFile = f'cf_avg_msd.{fileName}'

        # diffusing and bulk atom counters
        gb_atoms = 0
        bulk_atoms = 0

        # define two classes of atoms based on MSD
        chunk = len(jar) // 100
        atom_class = [0]*chunk
        for ii in range(1, chunk):
            tmp = float(jar[99*chunk+ii])
            if tmp > 3:
                gb_atoms += 1
                atom_class[ii] = 1
            else:
                bulk_atoms += 1

        print(gb_atoms, bulk_atoms)

        timesteps = []
        gb_diffs = []
        bulk_diffs = []
        for i in range(1, 100, 2):
            # initialize two different MSDs
            NgbMsd = 0
            NbulkMsd = 0
            # go through lines of a timestep
            for jj in range(1, chunk):
                tmp = float(jar[i*chunk+jj])
                if atom_class[jj]:
                    NgbMsd += tmp
                else:
                    NbulkMsd += tmp

            timesteps.append((i+1)*50000)
            gb_diffs.append(NgbMsd / gb_atoms)
            bulk_diffs.append(NbulkMsd / bulk_atoms)

        with open(writeFile, 'a') as f:
            for x, y, z in zip(timesteps, gb_diffs, bulk_diffs):
                f.write(str(x) + '\t' + str(y) + '\t' + str(z) + '\n')

if __name__ == '__main__':
    main()
