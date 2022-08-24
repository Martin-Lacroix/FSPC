# Environment variables

export CPU_PER_PROC=2
export INPUT=examples/damNcomp_2D/input.py
export INPUT=examples/streamNcomp_2D/input.py
# export INPUT=examples/staticNcomp_2D/input.py
# export INPUT=examples/MarcoLucio_2D/input.py
export INPUT=examples/SimoneMeduri_2D/input.py

# Clean output folder

rm -rf workspace
mkdir workspace

# Runs the code

export LD_PRELOAD=/lib/x86_64-linux-gnu/libmkl_def.so:/lib/x86_64-linux-gnu/libmkl_avx2.so:/lib/x86_64-linux-gnu/libmkl_core.so:/lib/x86_64-linux-gnu/libmkl_intel_lp64.so:/lib/x86_64-linux-gnu/libmkl_intel_thread.so:/lib/x86_64-linux-gnu/libiomp5.so

export MKL_NUM_THREADS=${CPU_PER_PROC}
export OMP_NUM_THREADS=${CPU_PER_PROC}
export OPTION="-map-by node:PE=${CPU_PER_PROC}"
mpiexec ${OPTION} -n 2 python main.py -k ${CPU_PER_PROC} ${INPUT}
