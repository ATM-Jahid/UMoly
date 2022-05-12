#!/usr/bin/env python3

import math
import argparse
from random import randint

parser = argparse.ArgumentParser(description='Replicate lammps input files!')
parser.add_argument('-l', '--latt', default=3.14, metavar='', help='lattice constant', type=float)
parser.add_argument('-a', '--tilt', default=310, metavar='', help='lattice tilt angle', type=int)
parser.add_argument('-x', '--xdim', default=50, metavar='', help='x dimension length', type=int)
parser.add_argument('-y', '--ydim', default=200, metavar='', help='y dimension length', type=int)
parser.add_argument('-z', '--zdim', default=50, metavar='', help='z dimension length', type=int)
parser.add_argument('-M', '--moly', default='0.22', metavar='', help='Molybdenum portion')
parser.add_argument('-t', '--temp', default='1200', metavar='', help='temperature in kelvin')
parser.add_argument('-D', '--defect', default='none', metavar='', help='introduce interstitial/vacancy')
parser.add_argument('-i', '--input', default='grain', metavar='', help='input file name')
parser.add_argument('-o', '--output', default='niarg', metavar='', help='output file name')
parser.add_argument('-n', '--number', default=1, metavar='', help='replication number', type=int)
args = parser.parse_args()

p = args.tilt // 100
q = (args.tilt % 100) // 10

lat2 = args.latt
# go deeper if lat1 is not within 3% of lat2
for i in range(5):
    m = 10**i
    n = round((10**i) * math.sqrt(p*p + q*q))
    lat1 = n * lat2 / m / math.sqrt(p*p + q*q)
    if abs(1 - lat1/lat2) < 0.03:
        lmn = math.gcd(m, n)
        m /= lmn
        n /= lmn
        break

# then find dimensions
k = n * args.latt
xh = k * (args.xdim//k + 1) / 2
yh = lat2 * (args.ydim//lat2 + 1) / 2
zh = k * (args.zdim//k + 1) / 2

with open(f'in.{args.input}', 'r') as f:
    jar = f.readlines()

if args.defect != 'none':
    if args.defect in 'interstitial':
        have_to_find = 'Interstitial'
    elif args.defect in 'vacancy':
        have_to_find = 'Vacancy'

    for i in range(0, len(jar)):
        if have_to_find in jar[i]:
            UnStart = i
            for j in range(i+2, len(jar)):
                if "######" in jar[j]:
                    UnEnd = j
                    break
            break

    for i in range(UnStart+3, UnEnd-1):
        jar[i] = jar[i].replace('#', '', 1)

jar = ''.join(jar)

jar = jar.replace('LAT1', f'{lat1}', 1)
jar = jar.replace('LAT2', f'{lat2}', 1)
jar = jar.replace('RUN', f'{p}', 1)
jar = jar.replace('RISE', f'{q}', 1)
jar = jar.replace('xHALF', f'{xh}', 1)
jar = jar.replace('yHALF', f'{yh}', 1)
jar = jar.replace('zHALF', f'{zh}', 1)
jar = jar.replace('MOLY', f'{args.moly}', 1)
jar = jar.replace('TEMP', f'{args.temp}', 1)

for x in range(args.number):
    foo = jar.replace('GRAIN', f'{args.output}{x+1}')
    foo = foo.replace('SEED', f'{randint(10000,99999)}', 1)
    with open(f'in.{args.output}{x+1}', 'w') as f:
        f.write(foo)
