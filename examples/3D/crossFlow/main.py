import os.path as path
import numpy as np
import FSPC

# Path to the solver input files

path_F = path.dirname(__file__) + '/input_F.lua'
path_S = path.dirname(__file__) + '/input_S.py'
FSPC.init_solver(path_F, path_S)

# Set the coupling algorithm

algorithm = FSPC.algorithm.MVJ(10)
FSPC.set_algorithm(algorithm)

# Set the interface interpolator

RBF = lambda r: np.square(r/0.01)*np.ma.log(r/0.01)
interpolator = FSPC.interpolator.RBF(RBF)
FSPC.set_interpolator(interpolator)

# Set the time step manager

step = FSPC.general.TimeStep(5e-4, 5e-4)
FSPC.set_time_step(step)

# Set the convergence manager

residual = FSPC.general.Residual(1e-6)
FSPC.set_mechanical_res(residual)

# Start the FSI simulation

algorithm.simulate(2)
FSPC.general.print_clock()