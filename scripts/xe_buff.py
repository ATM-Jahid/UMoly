#!/usr/bin/env python3

import sys

def main():
    # input "xe_pos" files
    files = sys.argv[1:]
    print(files)

    for file in files:
        extract(file)

def extract(file):
    with open(file, 'r') as f:
        jar = f.readlines()

    fileName = file[file.find('.')+1:]
    writeFile = f'xe_msd.{fileName}'

    N = int(jar[3])
    chunk = N + 9
    timesteps = len(jar) // chunk

    start = 20
    buffDiff = 10
    buffLen = 50
    xe_2d = [0]*buffLen; xe_3d = [0]*buffLen

    for b in range(start, timesteps-buffLen, buffDiff):
        r_init = []
        for line in jar[b*chunk+9: (b+1)*chunk]:
            tmp = line.split()
            r_init.append([float(x) for x in tmp[2:]])

        for j in range(buffLen):
            for ii in range(N):
                r_curr = [float(x) for x in jar[(b+j+1)*chunk+9+ii].split()[2:]]
                d2 = (r_curr[0] - r_init[ii][0]) ** 2 + (r_curr[2] - r_init[ii][2]) ** 2
                d3 = d2 + (r_curr[1] - r_init[ii][1]) ** 2

                # populate arrays with buffers
                xe_2d[j] += d2
                xe_3d[j] += d3

    numBuff = (timesteps - buffLen - start) // buffDiff + 1
    xe_2d = [x / N / numBuff for x in xe_2d]
    xe_3d = [x / N / numBuff for x in xe_3d]

    with open(writeFile, 'a') as f:
        f.write(f'#Number of buffers: {numBuff}\n' +
                f'#Xe in gb: {N}\n#Xe in bulk: 0\n' +
                '#Buffer averaged mean squared displacements\n' +
                '#gb_xe_2d gb_xe_3d\n0 0\n')
        for i in range(buffLen):
            f.write(f'{xe_2d[i]:.5} {xe_3d[i]:.5}\n')

if __name__ == '__main__':
    main()
