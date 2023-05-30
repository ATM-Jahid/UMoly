#!/usr/bin/env python

import math
import argparse
import random

parser = argparse.ArgumentParser(description='Replicate lammps input files! (in metal units)')
parser.add_argument('-l', '--latt', default=3.43, metavar='', help='lattice constant', type=float)
parser.add_argument('-x', '--xdim', default=40, metavar='', help='x dimension length (lattice unit)', type=int)
parser.add_argument('-y', '--ydim', default=40, metavar='', help='y dimension length (lattice unit)', type=int)
parser.add_argument('-z', '--zdim', default=40, metavar='', help='z dimension length (lattice unit)', type=int)
parser.add_argument('-M', '--moly', default=0.22, metavar='', help='molybdenum portion', type=float)
parser.add_argument('-X', '--xenon', default=700, metavar='', help='number of Xe atoms', type=int)
parser.add_argument('-r', '--bRad', default=20, metavar='', help='bubble radius (box unit)', type=float)
parser.add_argument('-s', '--bShl', default=10, metavar='', help='bubble shell depth (box unit)', type=float)
parser.add_argument('-p', '--pTyp', default=-1, metavar='', help='PKA type', type=int)
parser.add_argument('-d', '--pDis', default=50, metavar='', help='PKA distance from bubble (box unit)', type=float)
parser.add_argument('-e', '--pEn', default=100, metavar='', help='PKA energy', type=float)
parser.add_argument('-R', '--sRad', default=10, metavar='', help='thermal spike radius (box unit)', type=float)
parser.add_argument('-t', '--temp', default=400, metavar='', help='temperature in kelvin', type=float)
parser.add_argument('-i', '--input', default='cascade', metavar='', help='input file name')
parser.add_argument('-o', '--output', default='knock', metavar='', help='output file name')
parser.add_argument('-n', '--number', default=1, metavar='', help='replication number', type=int)
args = parser.parse_args()

if args.pTyp == -1:
	if random.random() > args.moly:
		pty = 1
	else:
		pty = 2
else:
	pty = args.pTyp

with open(f'in.{args.input}', 'r') as f:
    jar = f.readlines()

jar = ''.join(jar)

jar = jar.replace('__LATT', f'{args.latt}', 1)
jar = jar.replace('__xDIM', f'{args.xdim}', 1)
jar = jar.replace('__yDIM', f'{args.ydim}', 1)
jar = jar.replace('__zDIM', f'{args.zdim}', 1)
jar = jar.replace('__MOLY', f'{args.moly}', 1)
jar = jar.replace('__XENON', f'{args.xenon}', 1)
jar = jar.replace('__BUBBLE_RADIUS', f'{args.bRad}', 1)
jar = jar.replace('__BUBBLE_SHELL', f'{args.bShl}', 1)
jar = jar.replace('__PKA_TYPE', f'{pty}', 1)
jar = jar.replace('__PKA_DISTANCE', f'{args.pDis}', 1)
jar = jar.replace('__PKA_ENERGY', f'{args.pEn}', 1)
jar = jar.replace('__SPIKE_RADIUS', f'{args.sRad}', 1)
jar = jar.replace('__TEMP', f'{args.temp}', 1)

for x in range(args.number):
    foo = jar.replace('__CASCADE', f'{args.output}{x+1}')
    foo = foo.replace('__SEED', f'{random.randint(10000,99999)}', 1)
    with open(f'in.{args.output}{x+1}', 'w') as f:
        f.write(foo)
