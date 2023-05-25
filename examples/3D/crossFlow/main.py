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

# Configure the algorithm

algorithm = FSPC.MVJ(solver)
algorithm.interp = FSPC.RBF(solver,RBF)
algorithm.convergM = FSPC.Convergence(1e-6)
algorithm.step = FSPC.TimeStep(5e-4,0.01)

algorithm.endTime = 2
algorithm.endTime = 0.002
algorithm.omega = 0.5
algorithm.maxIter = 10

# Start the FSPC simulation

algorithm.simulate()
FSPC.printClock()