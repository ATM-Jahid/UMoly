#!/usr/bin/env python3

import sys

def main():
    # input "unwDump" files
    files = sys.argv[1:]
    print(files)

    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()

        fileName = file[file.find('.')+1:]
        writeFile = f'sqdi_last.{fileName}'

        N = int(jar[3])
        chunk = N + 9

        # the calculation can be done in one loop
        sqdi = [0]*N
        for ii in range(N):
            tmp1 = jar[9+ii].split()
            tmp2 = jar[100*chunk+9+ii].split()
            sqdi[ii] = [int(tmp1[1])]
            sqd = 0
            for jj in range(3):
                d = float(tmp2[2+jj]) - float(tmp1[2+jj])
                sqd += d * d
            sqdi[ii].append(sqd)

        with open(writeFile, 'a') as f:
            for ii in range(N):
                f.write(f'{sqdi[ii][0]} {sqdi[ii][1]}\n')

if __name__ == '__main__':
    main()
