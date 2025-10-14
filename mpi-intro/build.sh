#!/bin/bash

module add mpi/openmpi-x86_64

# EX 01
mpicc ./hello.c -o hello
# mpirun -np 8 ./hello
# mpirun ./hello

# Get number of cores
# nproc #24
# lscpu |grep Core #12

# Run the program with 24 processes on 4 hosts
$(which mpirun) -machinefile hosts -np 24 ./hello

# EX 02
# mpicc ./ring.c -o ring
# mpirun ./ring