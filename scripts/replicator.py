#!/usr/bin/env python3

import math
import argparse
from random import randint

parser = argparse.ArgumentParser(description='Replicate lammps input files!')
parser.add_argument('-l', '--latt', default=3.14, metavar='', help='lattice constant', type=float)
parser.add_argument('-a', '--tilt', default=310, metavar='', help='lattice tilt angle', type=int)
parser.add_argument('-x', '--xdim', default=50, metavar='', help='x dimension length', type=int)
parser.add_argument('-y', '--ydim', default=200, metavar='', help='y dimension length', type=int)
parser.add_argument('-z', '--zdim', default=12, metavar='', help='z dimension length', type=int)
parser.add_argument('-m', '--moly', default='0.22', metavar='', help='Molybdenum portion')
parser.add_argument('-t', '--temp', default='1200', metavar='', help='temperature in kelvin')
parser.add_argument('-i', '--input', default='grain', metavar='', help='input file name')
parser.add_argument('-o', '--output', default='niarg', metavar='', help='output file name')
parser.add_argument('-n', '--number', default=1, metavar='', help='replication number', type=int)
args = parser.parse_args()

p = int(args.tilt / 100)
q = int((args.tilt % 100) / 10)

k = args.latt * math.sqrt(p*p + q*q)
xh = k * (int(args.xdim/k) + 1) / 2
yh = k * (int(args.ydim/k) + 1) / 2
zh = args.latt * (int(args.zdim/args.latt) + 1) / 2

for x in range(args.number):
    with open(f'in.{args.input}', 'r') as f:
        jar = f.read()

    jar = jar.replace('LATT', f'{args.latt}', 1)
    jar = jar.replace('RUN', f'{p}', 1)
    jar = jar.replace('RISE', f'{q}', 1)
    jar = jar.replace('xHALF', f'{xh}', 1)
    jar = jar.replace('yHALF', f'{yh}', 1)
    jar = jar.replace('zHALF', f'{zh}', 1)
    jar = jar.replace('MOLY', f'{args.moly}', 1)
    jar = jar.replace('SEED', f'{randint(10000,99999)}', 1)
    jar = jar.replace('TEMP', f'{args.temp}', 1)
    jar = jar.replace('GRAIN', f'{args.output}{x+1}')

    with open(f'in.{args.output}{x+1}', 'w') as f:
        f.write(jar)
