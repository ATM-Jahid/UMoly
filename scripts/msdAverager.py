#!/usr/bin/env python3

import sys

foo = []
def extract(fileName):
    with open(fileName, 'r') as f:
        jar = f.readlines()
    foo.append(jar)

def average():
    writeFile = f'msd.avg-{folder[0][4:]}'
    with open(writeFile, 'w') as f:
        f.write(''.join(foo[0][:2]))

    for x in range(2, len(foo[0])):
        jar = []
        for y in range(len(folder)):
            jar.append([float(z) for z in foo[y][x].split()])

        for i in range(len(jar[0])):
            for j in range(1, len(jar)):
                jar[0][i] += jar[j][i]
            jar[0][i] /= len(jar)

        with open(writeFile, 'a') as f:
            f.write(' '.join([f'{c:.5f}' for c in jar[0]]))
            f.write('\n')

    print(writeFile)

if __name__ == "__main__":
    folder = sys.argv[1:]
    print(folder)
    for file in folder:
        extract(file)
    average()
