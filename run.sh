# Environment variables

export CPU_PER_PROC=4

export INPUT=examples/2D/elasticFunnel/input.py
export INPUT=examples/2D/damBreak/input.py
export INPUT=examples/2D/carsherWall/input.py
export INPUT=examples/2D/hydroStatic/input.py
export INPUT=examples/2D/freeStream/input.py
export INPUT=examples/2D/rubberGate/input.py
export INPUT=examples/2D/vonKarman/input.py
export INPUT=examples/2D/flowDrivenDisk/input.py
export INPUT=examples/2D/lockingPump/input.py

export INPUT=examples/3D/crossFlow/input.py
export INPUT=examples/3D/damBreak/input.py
export INPUT=examples/3D/hydroStatic/input.py
export INPUT=examples/3D/rubberGate/input.py

# Clean output folder

rm -rf workspace
mkdir workspace

# Runs the code

export MKL_NUM_THREADS=${CPU_PER_PROC}
export OMP_NUM_THREADS=${CPU_PER_PROC}
export OPTION="-map-by node:PE=${CPU_PER_PROC}"
mpiexec ${OPTION} -n 2 python main.py -k ${CPU_PER_PROC} ${INPUT}
