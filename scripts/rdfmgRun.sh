#!/bin/bash
#SBATCH -J "GRAIN"
#SBATCH -N 1
#SBATCH -n 32
#PBS -p gradq

date
pwd
printf "\n[[ in.GRAIN ]]\n\n"

module --ignore-cache load MPICH/3.2.1-GCC-7.2.0-2.29
mpirun -np 32 /home/ahasan3/bin/lmp -i in.GRAIN

printf "\nJob finished!\n"
date
