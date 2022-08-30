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
    y_xe = []; e_xe = []

    # input "umoxe_diff" files
    files = sys.argv[1:]
    for file in files:
        name, jar = extract(file)
        x.append(int(name[-3:]))

        tmp = jar.split()
        y_u.append(float(tmp[1]))
        e_u.append(float(tmp[2]))
        y_mo.append(float(tmp[3]))
        e_mo.append(float(tmp[4]))
        y_xe.append(float(tmp[5]))
        e_xe.append(float(tmp[6]))

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
    y_xe = [x for _, x in sorted(zip(tilt, y_xe))]
    e_xe = [x for _, x in sorted(zip(tilt, e_xe))]
    tilt = sorted(tilt)

    plt.figure(figsize=(5,4))
    plt.errorbar(tilt, y_u, e_u, color=plt.cm.jet(0.2), marker='o', ls= '-',
            elinewidth=3, capsize=5, capthick=1, label='U')
    plt.errorbar(tilt, y_mo, e_mo, color=plt.cm.jet(0.8), marker='v', ls='--',
            elinewidth=2, capsize=5, capthick=2, label='Mo')
    plt.errorbar(tilt, y_xe, e_xe, color=plt.cm.jet(0.5), marker='s', ls='-.',
            elinewidth=1, capsize=5, capthick=3, label='Xe')

    csl = [r'$\Sigma$41(190)', r'$\Sigma$13(150)', r'$\Sigma$5(130)',
            r'$\Sigma$5(120)', r'$\Sigma$17(350)', r'$\Sigma$25(340)']
    for i, txt in enumerate(csl):
        plt.annotate(txt, (tilt[i]-2, 4.2e-11), rotation=45)

    plt.xlim(0, 90)
    plt.ylim(0, 4.2e-11)
    plt.xlabel('Misorientation angle (deg)')
    plt.ylabel(r'Diffusivity (m$^2$s$^{-1}$)')
    plt.legend(loc='center right')
    plt.tight_layout()
    plt.savefig('dvstilt.pdf')

if __name__ == '__main__':
    main()
