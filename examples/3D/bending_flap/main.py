import os.path as path
import FSPC

# Path to the solver input files

path_F = path.dirname(__file__)+'/input_F.lua'
path_S = path.dirname(__file__)+'/input_S.py'
FSPC.init_solver(path_F, path_S)

# Set the coupling algorithm

algorithm = FSPC.algorithm.MVJ(10)
FSPC.set_algorithm(algorithm)

# Set the interface interpolator

interpolator = FSPC.interpolator.TPS(0.01)
FSPC.set_interpolator(interpolator)

# Set the time step manager

step = FSPC.general.TimeStep(5e-4, 5e-4)
FSPC.set_time_step(step)

# Set the convergence manager

residual = FSPC.general.Residual(1e-6)
FSPC.set_mechanical_res(residual)

# Start the fluid-structure simulation

algorithm.simulate(2)
FSPC.general.print_clock()