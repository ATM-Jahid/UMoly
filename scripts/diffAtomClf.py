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
        for ii in range(2, chunk):
            tmp = float(jar[99*chunk+ii].split()[3])
            if tmp > 3:
                gb_atoms += 1
                atom_class[ii] = 1
            else:
                bulk_atoms += 1

        print(gb_atoms, bulk_atoms)

        timesteps = []
        gb_diffs = []
        bulk_diffs = []
        tot_diffs = []
        for i in range(1, 100, 2):
            # initialize two different MSDs
            NgbMsd = 0
            NbulkMsd = 0
            Nmsd = 0
            # go through lines of a timestep
            for jj in range(2, chunk):
                tmp = float(jar[i*chunk+jj].split()[3])
                if atom_class[jj]:
                    NgbMsd += tmp
                    Nmsd += tmp
                else:
                    NbulkMsd += tmp
                    Nmsd += tmp

            timesteps.append(int(jar[i*chunk].split()[1]))
            gb_diffs.append(NgbMsd / gb_atoms)
            bulk_diffs.append(NbulkMsd / bulk_atoms)
            tot_diffs.append(Nmsd / (chunk - 2))

        with open(writeFile, 'a') as f:
            f.write('# Mean squared displacement data for classified atoms\n')
            f.write('# Timestep gb_avg bulk_avg tot_avg\n')
            for x, y, z, v in zip(timesteps, gb_diffs, bulk_diffs, tot_diffs):
                f.write(str(x) + '\t' + str(y) + '\t' + str(z) + '\t' + str(v) + '\n')

if __name__ == '__main__':
    main()
