# Number of CPU and threads

export NUN_THREADS=8
export CPU_PER_PROC=4

# Path to the external library

export PYTHONPATH=${PWD}:${PYTHONPATH}
export PYTHONPATH=${PWD}/../Metafor/oo_meta:${PYTHONPATH}
export PYTHONPATH=${PWD}/../Metafor/build/bin:${PYTHONPATH}
export PYTHONPATH=${PWD}/../PFEM3D/build/bin:${PYTHONPATH}

# Path to the Python script

export SCRIPT=${PWD}/examples/2D/carsherWall/main.py
# export SCRIPT=${PWD}/examples/2D/coolingDisk/main.py
# export SCRIPT=${PWD}/examples/2D/damBreak/main.py
# export SCRIPT=${PWD}/examples/2D/elasticFunnel/main.py
# export SCRIPT=${PWD}/examples/2D/flowDrivenDisk/main.py
# export SCRIPT=${PWD}/examples/2D/freeStream/main.py
# export SCRIPT=${PWD}/examples/2D/hydroStatic/main.py
# export SCRIPT=${PWD}/examples/2D/lockingPump/main.py
# export SCRIPT=${PWD}/examples/2D/rayleBenard/main.py
# export SCRIPT=${PWD}/examples/2D/rubberGate/main.py
# export SCRIPT=${PWD}/examples/2D/vonKarman/main.py

# export SCRIPT=${PWD}/examples/3D/crossFlow/main.py
# export SCRIPT=${PWD}/examples/3D/damBreak/main.py
# export SCRIPT=${PWD}/examples/3D/hydroStatic/main.py
# export SCRIPT=${PWD}/examples/3D/rubberGate/main.py

# Clean output folder

rm -rf workspace
mkdir workspace
cd workspace

# Runs the code

export MKL_NUM_THREADS=${NUN_THREADS}
export OMP_NUM_THREADS=${NUN_THREADS}
export OPTION="-map-by node:PE=${CPU_PER_PROC}"
mpiexec ${OPTION} -n 2 python ${SCRIPT} -k ${NUN_THREADS}