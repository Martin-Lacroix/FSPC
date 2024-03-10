import os.path as path
import numpy as np
import FSPC

# Input parameters for FSPC

R = 0.01
RBF = lambda r: np.square(r/R)*np.ma.log(r/R)
path_F = path.dirname(__file__)+'/input_F.lua'
path_S = path.dirname(__file__)+'/input_S.py'

# Initialize the simulation

FSPC.set_step(1e-3,0.01)
FSPC.set_thermal_res(1e-6)
FSPC.set_mechanical_res(1e-6)
FSPC.set_solver(path_F,path_S)
FSPC.set_interpolator(FSPC.interpolator.RBF,RBF)
FSPC.set_algorithm(FSPC.algorithm.MVJ,25)

# Start the FSPC simulation

FSPC.general.simulate(8)
FSPC.general.print_clock()