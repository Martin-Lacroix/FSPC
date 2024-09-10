# Path to the external library

export PYTHONPATH=${PWD}:${PYTHONPATH}
export PYTHONPATH=${PWD}/pyStream/build:${PYTHONPATH}
export PYTHONPATH=${PWD}/../Metafor/oo_meta:${PYTHONPATH}
export PYTHONPATH=${PWD}/../Metafor/oo_metaB/bin:${PYTHONPATH}
export PYTHONPATH=${PWD}/../PFEM3D/build/bin:${PYTHONPATH}

# Path to the Python script

# export SCRIPT=${PWD}/examples/2D/clamped_axisym/main.py
# export SCRIPT=${PWD}/examples/2D/clamped_beam/main.py
export SCRIPT=${PWD}/examples/2D/dam_break/main.py
# export SCRIPT=${PWD}/examples/2D/pipe_obstacle/main.py
# export SCRIPT=${PWD}/examples/2D/pipe_squeezed/main.py
# export SCRIPT=${PWD}/examples/2D/rubber_gate/main.py
# export SCRIPT=${PWD}/examples/2D/sloshing_flap/main.py
# export SCRIPT=${PWD}/examples/2D/thermo_disk/main.py
# export SCRIPT=${PWD}/examples/2D/thermo_square/main.py
# export SCRIPT=${PWD}/examples/2D/vertical_container/main.py
# export SCRIPT=${PWD}/examples/2D/von_karman/main.py

# export SCRIPT=${PWD}/examples/3D/bending_flap/main.py
# export SCRIPT=${PWD}/examples/3D/clamped_beam/main.py
# export SCRIPT=${PWD}/examples/3D/dam_break/main.py
# export SCRIPT=${PWD}/examples/3D/pipe_obstacle/main.py
# export SCRIPT=${PWD}/examples/3D/thermo_sphere/main.py
# export SCRIPT=${PWD}/examples/3D/sloshing_flap/main.py

# Clean output folder

rm -rf workspace
mkdir workspace
cd workspace

# Run and export the workspace

export CPU_PER_PROC=4
export THR_PER_PROC=8
export MKL_NUM_THREADS=${THR_PER_PROC}
export OMP_NUM_THREADS=${THR_PER_PROC}
export OPTION="-map-by node:PE=${CPU_PER_PROC}"
mpiexec ${OPTION} -n 2 python3 ${SCRIPT} -k ${THR_PER_PROC} 2>&1 | tee workspace.txt

# Run the test battery

# python3 ../battery.py
