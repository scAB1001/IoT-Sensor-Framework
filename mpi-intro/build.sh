#!/bin/bash

module add mpi/openmpi-x86_64

# EX 01
# mpicc ./hello.c -o hello
# mpirun ./hello

# lscpu |grep Core #12
# $(which mpirun) -machinefile hosts -np 24 ./hello

# EX 02
mpicc ./ring.c -o ring
mpirun ./ring