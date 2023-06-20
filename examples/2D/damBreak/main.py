import os.path as path
import FSPC

# %% Input Parameters for FSPC

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

import numpy as np
RBF = lambda r: np.square(r)*np.ma.log(r)

# %% Initialize the Manager Module

FSPC.Manager.step = FSPC.TimeStep(1e-3,1e-2)
FSPC.Manager.convMecha = FSPC.Convergence(1e-8)
FSPC.Manager.solver = FSPC.getSolver(pathF,pathS)
FSPC.Manager.interp = FSPC.RBF(RBF)

# Configure the algorithm

algorithm = FSPC.MVJ()
algorithm.maxIter = 25
algorithm.endTime = 1
algorithm.omega = 0.5

# Start the FSPC simulation

algorithm.simulate()
FSPC.printClock()