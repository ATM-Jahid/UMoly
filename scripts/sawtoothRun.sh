#!/bin/bash
#PBS -N GRAIN
#PBS -l select=1:ncpus=48:mpiprocs=48
#PBS -l walltime=10:00
#PBS -j oe
#PBS -P mmm

cd $PBS_O_WORKDIR
echo $PBS_NODEFILE
module load lammps/7jan22

date
pwd
printf "\n[[ in.GRAIN ]]\n\n"

mpirun lmp -i in.GRAIN

printf "\nJob finished!\n"
date
