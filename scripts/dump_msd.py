#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt

files = sys.argv[1:]
print(files)

for file in files:
    with open(file, 'r') as f:
        jar = f.readlines()

    num_atoms = jar[3]
    box = jar[5*(num_atoms+9)+5: 5*(num_atoms+9)+8]
    blo, bhi = [[0]*3, [0]*3]
    for i in range(3):
        blo[i], bhi[i] = [float(x) for x in box[i].split()]

