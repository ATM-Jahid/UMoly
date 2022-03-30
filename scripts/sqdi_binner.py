#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt

files = sys.argv[1:]
print(files)

for file in files:
    with open(file, 'r') as f:
        jar = f.readlines()

    num_ts = 100
    offset = 2
    chunk = len(jar) // num_ts
    jar = [float(x.split()[3]) for x in jar[(num_ts-1)*chunk+offset:]]

    binwidth = 0.5
    binlist = np.arange(min(jar), max(jar)+binwidth, binwidth)
    plt.hist(jar, binlist)

plt.show()
