# Environment variables

export CPU_PER_PROC=2
export INPUT=examples/damNcomp/input.py

# Clean output folder

rm -rf workspace
mkdir workspace

# Runs the code

export MKL_NUM_THREADS=${CPU_PER_PROC}
export OMP_NUM_THREADS=${CPU_PER_PROC}
export OPTION="-map-by node:PE=${CPU_PER_PROC}"
mpiexec ${OPTION} -n 2 python3 main.py -k ${CPU_PER_PROC} ${INPUT}