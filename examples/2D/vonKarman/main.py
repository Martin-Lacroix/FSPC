from interpolator import TEST
import os.path as path
import numpy as np
import FSPC

# %% Paths to the input files

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# %% Fluid Structure Coupling

process = FSPC.Process()
solver = process.getSolver(pathF,pathS)
RBF = lambda r: np.square(r)*np.ma.log(r)
initPos = solver.getPosition()

# Configure the algorithm

algorithm = FSPC.MVJ(solver)
# algorithm.interp = TEST(solver,9)
algorithm.interp = FSPC.KNN(solver,1)
algorithm.convergM = FSPC.Convergence(1e-6)
algorithm.step = FSPC.TimeStep(1e-2,1e-2)

algorithm.endTime = 15
algorithm.omega = 0.5
algorithm.maxIter = 25

# Start the FSPC simulation

algorithm.simulate()
FSPC.printClock()
