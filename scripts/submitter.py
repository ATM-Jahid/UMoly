#!/usr/bin/env python3

import os
import sys

def copier(fileName):
    with open('rdfmgRun.sh', 'r') as f:
        jar = f.read()

    fileName = fileName[fileName.find('.')+1:]
    jar = jar.replace('GRAIN', fileName)

    writeFile = f'sub_{fileName}.sh'
    with open(writeFile, 'w') as f:
        f.write(jar)
    os.chmod(writeFile, 0o755)

    if not dry:
        os.system(f'sbatch {writeFile}')

if __name__ == "__main__":
    folder = sys.argv[1:]
    if '-d' in folder:
        folder.remove('-d')
        dry = 1
    else:
        dry = 0
    print(folder)
    for file in folder:
        copier(file)
