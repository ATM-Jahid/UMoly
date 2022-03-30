#!/usr/bin/env python3

import sys

def main():
    files = sys.argv[1:]
    print(files)

    file1 = files[0]
    fileName = file1[file1.find('.')+1:-2]
    writeFile = f'crude_diff.{fileName}'

    diffs_gb = []
    diffs_bulk = []
    diff_atoms = []

    for file in files:
        with open(file, 'r') as f:
            jar = f.readlines()

        num_ts = 100
        offset = 2
        chunk = len(jar) // num_ts
        jar = [float(x.split()[3]) for x in jar[(num_ts-1)*chunk+offset:]]
        foo = []; bar = []
        for x in jar:
            if x > 3:
                foo.append(x)
            else:
                bar.append(x)

        diff_atoms.append(len(foo))
        diffs_gb.append(sum(foo)/len(foo))
        diffs_bulk.append(sum(bar)/len(bar))

    with open(writeFile, 'a') as f:
        f.write('num_diff\tgb_diff\tbulk_diff\n')
        for n, g, b in zip(diff_atoms, diffs_gb, diffs_bulk):
            f.write(f'{n}\t{g}\t{b}\n')

if __name__ == '__main__':
    main()
