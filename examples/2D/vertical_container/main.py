import FSPC
import os

# Path to the solver input files

base = os.path.dirname(__file__)
FSPC.init_solver(f'{base}/input_F.lua', f'{base}/input_S.py')

# Set the coupling algorithm

algorithm = FSPC.algorithm.MVJ(65)
FSPC.set_algorithm(algorithm)

# Set the interface interpolator

interpolator = FSPC.interpolator.TPS(0.1)
FSPC.set_interpolator(interpolator)

# Set the time step manager

step = FSPC.general.TimeStep(1e-3, 1e-2)
FSPC.set_time_step(step)

# Set the convergence manager

residual = FSPC.general.Residual(1e-6)
FSPC.set_mechanical_res(residual)

# Start the fluid-structure simulation

algorithm.simulate(10)
FSPC.general.print_clock()

# Compare the results with a reference solution

os.system(f'python3 {base}/battery.py')