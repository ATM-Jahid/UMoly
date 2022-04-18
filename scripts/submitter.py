#!/usr/bin/env python3

import os
import sys

def copier(clusterName, fileName):
    if clusterName in 'rdfmg':
        c = 0
        scriptFile = 'rdfmgRun.sh'
    elif clusterName in 'sawtooth':
        c = 1
        scriptFile = 'sawtoothRun.sh'
    with open(scriptFile, 'r') as f:
        jar = f.read()

    fileName = fileName[fileName.find('.')+1:]
    jar = jar.replace('GRAIN', fileName)

    writeFile = f'sub_{fileName}.sh'
    with open(writeFile, 'w') as f:
        f.write(jar)
    os.chmod(writeFile, 0o755)

    if not dry:
        if c == 0:
            os.system(f'sbatch {writeFile}')
        elif c == 1:
            os.system(f'qsub {writeFile}')

if __name__ == "__main__":
    arguments = sys.argv[1:]
    if '-d' in arguments:
        arguments.remove('-d')
        dry = 1
    else:
        dry = 0
    cluster = arguments[0]
    files = arguments[1:]
    print(files)
    for file in files:
        copier(cluster, file)
