# Environment variables

export INPUT=examples/damNcomp/input.py

# Clean output folder

rm -rf workspace
mkdir workspace

# Runs the code

export MKL_NUM_THREADS=4
export OMP_NUM_THREADS=4
export OMP_PROC_BIND=true

mpiexec -n 2 python3 main.py -k 4 ${INPUT}