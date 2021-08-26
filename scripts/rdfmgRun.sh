#!/bin/bash
#SBATCH -J "GRAIN"
#SBATCH -N 1
#SBATCH -n 64

date
pwd
printf "\n[[ in.GRAIN ]]\n\n"

mpirun /home/ahasan3/bin/lmp -i in.GRAIN

printf "\nJob finished!\n"
date
