#!/usr/bin/env python3

import sys
from statistics import mean, stdev

def extract(readFile, writeFile):
    with open(readFile, 'r') as f:
        jar = f.readlines()
    jar = jar[2:]
    temp = int(readFile[readFile.find('at')+2:readFile.find('/')])

    x = []; z = []; r = []
    for line in jar:
        tmp = line.split()
        x.append(float(tmp[0]))
        z.append(float(tmp[2]))
        r.append(float(tmp[3]))

    x_mean, x_std = mean(x), stdev(x)
    z_mean, z_std = mean(z), stdev(z)
    r_mean, r_std = mean(r), stdev(r)

    if z_mean/x_mean < 0.5 or x_mean/z_mean < 0.5:
        xi = 1
    else:
        xi = 2

    to_pico = 1/0.002
    to_si = 1e-8
    diff = 1 / 2 / xi * r_mean * to_pico * to_si
    devi = 1 / 2 / xi * r_std * to_pico * to_si

    with open(writeFile, 'a') as f:
        f.write(f'{temp}\t{xi}\t{diff}\t{devi}\n')

def main():
    files = sys.argv[1:]
    print(files)

    file1 = files[0]
    fileName = file1[:file1.find('at')]
    writeFile = f'diffusivities_{fileName}'

    with open(writeFile, 'a') as f:
        f.write(f'# Diffusivities for {fileName}\n')
        f.write('# temp dim. mean stdev\n')

    for file in files:
        extract(file, writeFile)

if __name__ == '__main__':
    main()
