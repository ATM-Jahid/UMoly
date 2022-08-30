#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True

def main():
    # input "sqdi_last" files
    files = sys.argv[1:]
    print(files)

    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()

        jar = [float(x.split()[1]) for x in jar]

        binwidth = 1.0
        binlist = np.arange(min(jar), max(jar)+binwidth, binwidth)

        plt.figure(figsize=(5,4))
        plt.hist(jar, binlist, color=plt.cm.viridis(0.5))
        plt.xlabel(r'$r^2$ (\r{A}$^2$)')
        plt.ylabel('Count')
        plt.xlim(0, 60)
        plt.ylim(0, 300)
        plt.tight_layout()
        plt.savefig('histogram.pdf')

if __name__ == '__main__':
    main()
