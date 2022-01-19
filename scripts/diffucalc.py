#!/usr/bin/env python3

import os
import sys
import statistics
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

folders = sys.argv[1:]
print(folders)
temperatures = []
diffusivities = []

for folder in folders:
    # getting the temperature
    temp_ind = folder.find('at') + 2
    temperatures.append(int(folder[temp_ind:]))
    os.chdir(folder)

    # sorting out necessary output files
    files = os.listdir()
    msd_files = sorted([x for x in files if 'msd.' in x])
    xyz_files = sorted([x for x in files if 'xyz.' in x])
    relax_files = sorted([x for x in files if 'relax.' in x])

    slopes = []
    # looping over single simulation
    for f1, f2, f3 in zip(msd_files, xyz_files, relax_files):
        with open(f1, 'r') as f:
            msd_jar = f.readlines()
        with open(f2, 'r') as f:
            xyz_jar = f.readlines()
        with open(f3, 'r') as f:
            relax_jar = f.readlines()

        # getting msd values over 8 nanoseconds
        step = []
        bar = []
        msd_jar = msd_jar[11:]
        for x in msd_jar:
            step.append(float(x.split()[0]))
            bar.append(float(x.split()[9]))

        # getting a linear fit
        m, b = np.polyfit(step, bar, 1)
        slopes.append(m)
    # averaging values from different seeds
    mean = statistics.mean(slopes)

    # getting length perpendicular to the GB
    Ly = float(relax_jar[-1].split()[6])
    diffusivities.append(Ly / 32 * mean * 1e-6)

    # moving back to main directory
    os.chdir('../')

# sorting with temperatures
z = [(x, y) for x, y in sorted(zip(temperatures, diffusivities))]
temper = [i for i,_ in z]
diffus = [j for _,j in z]
for i, j in zip(temper, diffus):
    print(i, j)

# plotting the pairs
overT = [1/T for T in temper]
logD = [np.log(D) for D in diffus]
plt.scatter(overT, logD)
plt.plot(overT, logD, 'r')
plt.show()
