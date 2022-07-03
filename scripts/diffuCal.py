#!/usr/bin/env python3

import sys
from statistics import mean, stdev

def extract(readFile, writeFile):
    with open(readFile, 'r') as f:
        jar = f.readlines()
    jar = jar[2:]
    temp = int(readFile[readFile.find('at')+2:readFile.find('/')])

    u = []; mo = []; tot = []
    for line in jar:
        tmp = line.split()
        if 'U' in tmp[0]:
            u.append(float(tmp[1]))
        elif 'Mo' in tmp[0]:
            mo.append(float(tmp[1]))
        elif 'Tot' in tmp[0]:
            tot.append(float(tmp[1]))

    u_mean, u_std = mean(u), stdev(u)
    mo_mean, mo_std = mean(mo), stdev(mo)
    tot_mean, tot_std = mean(tot), stdev(tot)

    xi = 2
    to_pico = 1e-5/0.002
    to_si = 1e-8

    diff_u = 1 / 2 / xi * u_mean * to_pico * to_si
    devi_u = 1 / 2 / xi * u_std * to_pico * to_si
    diff_mo = 1 / 2 / xi * mo_mean * to_pico * to_si
    devi_mo = 1 / 2 / xi * mo_std * to_pico * to_si
    diff_tot = 1 / 2 / xi * tot_mean * to_pico * to_si
    devi_tot = 1 / 2 / xi * tot_std * to_pico * to_si

    with open(writeFile, 'a') as f:
        f.write(f'{temp} {diff_u:e} {devi_u:e} ' +
                f'{diff_mo:e} {devi_mo:e} ' +
                f'{diff_tot:e} {devi_tot:e}\n')

def main():
    # input "./clf_slopes" files
    files = sys.argv[1:]
    print(files)

    file1 = files[0]
    fileName = file1[:file1.find('at')]
    writeFile = f'diffusivities_{fileName}'

    with open(writeFile, 'a') as f:
        f.write(f'# Diffusivities for {fileName}\n' +
                '# temp U_mean U_stdev Mo_mean Mo_stdev Tot_mean Tot_stdev\n')

    for file in files:
        extract(file, writeFile)

if __name__ == '__main__':
    main()
