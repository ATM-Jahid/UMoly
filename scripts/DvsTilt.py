#!/usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True

def extract(file):
    with open(file, 'r') as f:
        jar = f.readlines()

    # only plot 1200 K values
    jar = jar[-1]
    fileName = file[file.find('s.')+2:]
    return fileName, jar

def main():
    x = []
    y_u = []; e_u = []
    y_mo = []; e_mo = []

    # input "diffusivities" files
    files = sys.argv[1:]
    for file in files:
        name, jar = extract(file)
        x.append(int(name[-3:]))

        tmp = jar.split()
        y_u.append(float(tmp[1]))
        e_u.append(float(tmp[2]))
        y_mo.append(float(tmp[3]))
        e_mo.append(float(tmp[4]))

    # compute misorientation angles
    tilt = []
    for i in x:
        p = i // 100
        q = (i % 100) // 10
        tilt.append(360 * np.arctan(p/q) / np.pi)

    y_u = [x for _, x in sorted(zip(tilt, y_u))]
    e_u = [x for _, x in sorted(zip(tilt, e_u))]
    y_mo = [x for _, x in sorted(zip(tilt, y_mo))]
    e_mo = [x for _, x in sorted(zip(tilt, e_mo))]
    tilt = sorted(tilt)

    plt.figure(figsize=(5,4))
    plt.errorbar(tilt, y_u, e_u, color=plt.cm.seismic(0.7),
            marker='s', ls= '-', capsize=5, label='U')
    plt.errorbar(tilt, y_mo, e_mo, color=plt.cm.seismic(0.3),
            marker='v', ls='--', capsize=5, label='Mo')

    csl = [r'$\Sigma$41(190)', r'$\Sigma$13(150)', r'$\Sigma$5(130)',
            r'$\Sigma$5(120)', r'$\Sigma$17(350)', r'$\Sigma$25(340)']
    for i, txt in enumerate(csl):
        plt.annotate(txt, (tilt[i]-2, 4e-11), rotation=45)

    plt.xlim(0, 90)
    plt.ylim(0, 4e-11)
    plt.xlabel('Misorientation angle (deg)')
    plt.ylabel(r'Diffusivity (m$^2$s$^{-1}$)')
    plt.legend(loc='center right')
    plt.savefig('dvstilt.pdf')
    plt.show()

if __name__ == '__main__':
    main()
