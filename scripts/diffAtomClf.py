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
        num_gb_atoms = 0
        num_bulk_atoms = 0

        # define two classes of atoms based on MSD
        chunk = len(jar) // 100
        atom_class = [0]*chunk
        for ii in range(2, chunk):
            tmp = float(jar[99*chunk+ii].split()[3])
            if tmp > 3:
                num_gb_atoms += 1
                atom_class[ii] = 1
            else:
                num_bulk_atoms += 1

        print(num_gb_atoms, num_bulk_atoms)

        timesteps = []
        gb_X_diff = []; gb_Y_diff = []; gb_Z_diff = []
        gb_R_diff = []
        bulk_R_diff = []
        all_R_diff = []
        for i in range(1, 100, 2):
            # initialize two different MSDs
            Ngb_X_msd = 0
            Ngb_Y_msd = 0
            Ngb_Z_msd = 0
            Ngb_R_msd = 0
            Nbulk_R_msd = 0
            Nall_R_msd = 0
            # go through lines of a timestep
            for jj in range(2, chunk):
                line = jar[i*chunk+jj].split()
                if atom_class[jj]:
                    Ngb_X_msd += float(line[0])
                    Ngb_Y_msd += float(line[1])
                    Ngb_Z_msd += float(line[2])
                    Ngb_R_msd += float(line[3])
                    Nall_R_msd += float(line[3])
                else:
                    Nbulk_R_msd += float(line[3])
                    Nall_R_msd += float(line[3])

            timesteps.append(int(jar[i*chunk].split()[1]))
            gb_X_diff.append(Ngb_X_msd / num_gb_atoms)
            gb_Y_diff.append(Ngb_Y_msd / num_gb_atoms)
            gb_Z_diff.append(Ngb_Z_msd / num_gb_atoms)
            gb_R_diff.append(Ngb_R_msd / num_gb_atoms)
            bulk_R_diff.append(Nbulk_R_msd / num_bulk_atoms)
            all_R_diff.append(Nall_R_msd / (chunk - 2))

        with open(writeFile, 'a') as f:
            f.write('# Mean squared displacement data for classified atoms\n')
            f.write('# Timestep gb_X_avg gb_Y_avg gb_Z_avg gb_R_avg bulk_R_avg all_R_avg\n')
            for t, x, y, z, r, b, a in zip(timesteps, gb_X_diff, gb_Y_diff, gb_Z_diff,
                                            gb_R_diff, bulk_R_diff, all_R_diff):
                f.write(str(t) + '\t' + str(x) + '\t' + str(y) + '\t' + str(z) + '\t'
                        + str(r) + '\t' + str(b) + '\t' + str(a) + '\n')

if __name__ == '__main__':
    main()
