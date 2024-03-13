import os.path as path
import FSPC

# Path to the solver input files

path_F = path.dirname(__file__) + '/input_F.lua'
path_S = path.dirname(__file__) + '/input_S.py'

# Initialize the fluid and solid solvers

FSPC.set_mechanical_res(1e-6)
FSPC.set_time_step(1e-3, 0.01)
FSPC.init_solver(path_F, path_S)

# Set the interpolator and algorithm

interpolator = FSPC.interpolator.KNN(1)
FSPC.set_interpolator(interpolator)

algorithm = FSPC.algorithm.MVJ(25)
FSPC.set_algorithm(algorithm)

# Start the FSI simulation

algorithm.simulate(2)
FSPC.general.print_clock()