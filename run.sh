# Environment variables

export CPU_PER_PROC=4
# export INPUT=examples/damNcomp_2D/input.py
# export INPUT=examples/damNcomp_3D/input.py
# export INPUT=examples/streamNcomp_2D/input.py
# export INPUT=examples/staticNcomp_2D/input.py
# export INPUT=examples/staticNcomp_3D_RBF/input.py
# export INPUT=examples/MarcoLucio_2D_RBF/input.py
# export INPUT=examples/MarcoLucio_3D_RBF/input.py
export INPUT=examples/SimoneMeduri_2D_RBF/input.py
# export INPUT=examples/ZiFeiMeng_2D_RBF/input.py
# export INPUT=examples/ZiFeiMeng_3D_RBF/input.py
# export INPUT=examples/GuiFourey_2D/input.py
# export INPUT=examples/StefanTurek_2D_RBF/input.py

# Clean output folder

rm -rf workspace
mkdir workspace

# Runs the code

export MKL_NUM_THREADS=${CPU_PER_PROC}
export OMP_NUM_THREADS=${CPU_PER_PROC}
export OPTION="-map-by node:PE=${CPU_PER_PROC}"
mpiexec ${OPTION} -n 2 python main.py -k ${CPU_PER_PROC} ${INPUT}
