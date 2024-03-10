import os.path as path
import FSPC

# Input parameters for FSPC

path_F = path.dirname(__file__)+'/input_F.lua'
path_S = path.dirname(__file__)+'/input_S.py'

# Initialize the simulation

FSPC.set_step(1e-3,0.01)
FSPC.set_mechanical_res(1e-6)
FSPC.set_solver(path_F,path_S)
FSPC.set_interpolator(FSPC.interpolator.KNN,1)
FSPC.set_algorithm(FSPC.algorithm.MVJ,25)

# Start the FSPC simulation

FSPC.general.simulate(2)
FSPC.general.print_clock()