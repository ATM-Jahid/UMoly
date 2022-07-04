#!/usr/bin/env python3

import sys
from statistics import mean, stdev

def extract(readFile, writeFile):
    with open(readFile, 'r') as f:
        jar = f.readlines()
    jar = jar[2:]
    temp = int(readFile[readFile.find('at')+2:readFile.find('/')])

    xe = []
    for line in jar:
        tmp = line.split()
        xe.append(float(tmp[1]))

    xe_mean, xe_std = mean(xe), stdev(xe)

    xi = 2
    to_pico = 1e-5/0.002
    to_si = 1e-8

    diff_xe = 1 / 2 / xi * xe_mean * to_pico * to_si
    devi_xe = 1 / 2 / xi * xe_std * to_pico * to_si

    with open(writeFile, 'a') as f:
        f.write(f'{temp} {diff_xe:e} {devi_xe:e}\n')

def main():
    # input "./xe_slopes" files
    files = sys.argv[1:]
    print(files)

    file1 = files[0]
    fileName = file1[:file1.find('at')]
    writeFile = f'xe_diff.{fileName}'

    with open(writeFile, 'a') as f:
        f.write(f'# Xe diffusivities for {fileName}\n' +
                '# temp Xe_mean Xe_stdev\n')

    for file in files:
        extract(file, writeFile)

if __name__ == '__main__':
    main()
