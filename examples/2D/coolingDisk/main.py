import os.path as path
import FSPC

# %% Input Parameters for FSPC

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# %% Initialize the Manager Module

FSPC.Manager.step = FSPC.TimeStep(1e-2,0.01)
FSPC.Manager.convMecha = FSPC.Convergence(1e-8)
FSPC.Manager.convTherm = FSPC.Convergence(1e-6)
FSPC.Manager.solver = FSPC.getSolver(pathF,pathS)
FSPC.Manager.interp = FSPC.KNN(2)

# Configure the algorithm

algorithm = FSPC.ILS()
algorithm.maxIter = 25
algorithm.endTime = 8
algorithm.omega = 0.5

# Start the FSPC simulation

algorithm.simulate()
FSPC.printClock()