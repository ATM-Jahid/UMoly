#!/bin/bash
#PBS -N __CASCADE
#PBS -l select=6:ncpus=48:mpiprocs=48:ompthreads=1
#PBS -l walltime=24:00:00
#PBS -j oe
#PBS -P mmm

cd $PBS_O_WORKDIR
echo $PBS_NODEFILE
module load openmpi/4.1.5_ucx1.14.1

date
pwd
printf "\n[[ in.__CASCADE ]]\n\n"

mpirun /home/hasaatmj/builds/lammps/build/lmp -i in.__CASCADE

printf "\nJob finished!\n"
date
