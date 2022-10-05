#!/usr/bin/env python3

import sys

def main():
    # input "unwDump" files
    # "sqdi_last" filenames are inherited from unwDump
    files = sys.argv[1:]
    print(files)

    for file in files:
        extract(file)

def extract(file):
    with open(file, 'r') as f:
        jar = f.readlines()

    fileName = file[file.find('.')+1:]
    sqdiFile = f'sqdi_last.{fileName}'
    writeFile = f'buff_xyz.{fileName}'

    N = int(jar[3])
    chunk = N + 9
    timesteps = len(jar) // chunk

    with open(sqdiFile, 'r') as f:
        foo = f.readlines()
    for i in range(len(foo)):
        tmp = foo[i].split()
        # the condition below is different in buffer
        foo[i] = [int(tmp[0]), float(tmp[1]) > 3]

    num_tot = 0; num_gb_u = 0; num_gb_mo = 0
    for line in foo:
        if line[1]:               # gb
            num_tot += 1
            if line[0] == 1:        # U in gb
                num_gb_u += 1
            elif line[0] == 2:      # Mo in gb
                num_gb_mo += 1

    buffDiff = 10
    buffLen = 50
    u_x = [0.0]*buffLen; u_y = [0.0]*buffLen; u_z = [0.0]*buffLen
    mo_x = [0.0]*buffLen; mo_y = [0.0]*buffLen; mo_z = [0.0]*buffLen
    tot_x = [0.0]*buffLen; tot_y = [0.0]*buffLen; tot_z = [0.0]*buffLen

    start = 20
    for b in range(start, timesteps-buffLen, buffDiff):
        r_init = []
        for line in jar[b*chunk+9: (b+1)*chunk]:
            tmp = line.split()
            r_init.append([float(x) for x in tmp[2:]])

        for j in range(buffLen):
            for ii in range(N):
                r_curr = [float(x) for x in jar[(b+j+1)*chunk+9+ii].split()[2:]]
                if foo[ii][1]:                   # gb
                    x2 = (r_curr[0] - r_init[ii][0]) ** 2
                    y2 = (r_curr[1] - r_init[ii][1]) ** 2
                    z2 = (r_curr[2] - r_init[ii][2]) ** 2
                    tot_x[j] += x2; tot_y[j] += y2; tot_z[j] += z2
                    if foo[ii][0] == 1:         # U in gb
                        u_x[j] += x2; u_y[j] += y2; u_z[j] += z2
                    elif foo[ii][0] == 2:       # Mo in gb
                        mo_x[j] += x2; mo_y[j] += y2; mo_z[j] += z2

    numBuff = (timesteps - buffLen - start) // buffDiff + 1

    # per atom quantities
    tot_xpa = [x / num_tot / numBuff for x in tot_x]
    tot_ypa = [x / num_tot / numBuff for x in tot_y]
    tot_zpa = [x / num_tot / numBuff for x in tot_z]
    # avoid "div by zero" error
    if num_gb_u:
        u_xpa = [x / num_gb_u / numBuff for x in u_x]
        u_ypa = [x / num_gb_u / numBuff for x in u_y]
        u_zpa = [x / num_gb_u / numBuff for x in u_z]
    if num_gb_mo:
        mo_xpa = [x / num_gb_u / numBuff for x in mo_x]
        mo_ypa = [x / num_gb_u / numBuff for x in mo_y]
        mo_zpa = [x / num_gb_u / numBuff for x in mo_z]

    with open(writeFile, 'a') as f:
        f.write(f'#Number of buffers: {numBuff}\n' +
                f'#U in gb: {num_gb_u}\n#Mo in gb: {num_gb_mo}\n' +
                '#Buffer averaged directional MSDs in GB\n' +
                '#u_x2 u_y2 u_z2 mo_x2 mo_y2 mo_z2 tot_x2 tot_y2 tot_z2\n' +
                '0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0\n')
        for i in range(buffLen):
            f.write(f'{u_xpa[i]:.5} {u_ypa[i]:.5} {u_zpa[i]:.5} ' +
                    f'{mo_xpa[i]:.5} {mo_ypa[i]:.5} {mo_zpa[i]:.5} ' +
                    f'{tot_xpa[i]:.5} {tot_ypa[i]:.5} {tot_zpa[i]:.5}\n')

if __name__ == '__main__':
    main()
