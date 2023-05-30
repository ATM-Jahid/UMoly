#!/usr/bin/env python

import sys
import copy

def crunch(new, old, writeFile):
    # vector to be dumped
    r_dump = []

    # storing new positions to compute distances
    n2 = int(new[3])
    r_new = [0]*(n2+2)
    for line in new[9:]:
        tmp = line.split()
        ii = int(tmp[0])
        r_new[ii] = [float(x) for x in tmp[2:]]

    # get the dimensions for periodic boundary checks
    dim = []
    for k in range(3):
        dim.append(float(old[5+k].split()[1]))

    # compare old values, no need to store
    for line in old[9:]:
        tmp = line.split()
        ii = int(tmp[0])
        if r_new[ii] == 0:
            continue

        # this needs checks for periodic boundaries
        for k in range(3):
            if r_new[ii][k] - float(tmp[k+2]) > dim[k]/2:
                r_new[ii][k] -= dim[k]
            elif r_new[ii][k] - float(tmp[k+2]) < - dim[k]/2:
                r_new[ii][k] += dim[k]

        # compute squared distance
        d2 = 0
        for jj in range(3):
            d2 += (r_new[ii][jj] - float(tmp[jj+2]))**2

        # select atoms based on sq. distance
        if d2 > 5:
            pb = [ii, int(tmp[1])]
            for k in range(3):
                pb.append(float(tmp[k+2]))
            pb = [*pb, *r_new[ii]]
            r_dump.append(pb)

    # dump defect information
    with open(writeFile, 'a') as f:
        f.write(f'ITEM: init end diff\n' +
                f'{int(old[1])} {int(new[1])} {int(new[1]) - int(old[1])}\n' +
                f'ITEM: number of atoms\n' +
                f'{len(r_dump)}\n' +
                f'ITEM: id type x1 y1 z1 x2 y2 z2\n')
        for x in r_dump:
            for xx in x:
                f.write(f'{xx} ')
            f.write('\n')


def extract(dat, fileName):
    # write into a file
    writeFile = fileName[fileName.find('Def')+4:] + '.pdump'
    print(writeFile)

    A = 1  # start frame
    K = 5  # consider every kth frame

    ld = len(dat)
    curline = 0

    def skip(c, line):
        for i in range(c):
            n = int(dat[line+3])
            line += n + 9

            if line == ld:
                break

        return line

    curline = skip(A, curline)

    # init frame using curline
    natom = int(dat[curline+3])
    old = dat[curline:curline+natom+9]

    while True:
        # skip K frames
        curline = skip(K, curline)
        if curline == ld:
            break

        # end frame using curline
        natom = int(dat[curline+3])
        new = dat[curline:curline+natom+9]

        # compute using init and end
        crunch(new, old, writeFile)

        # make new old
        old = copy.deepcopy(new)


def main():
    files = sys.argv[1:]

    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()

        extract(jar, file)

if __name__ == '__main__':
    main()
