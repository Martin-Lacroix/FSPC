import os.path as path
import FSPC

# %% Paths to the input files

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# %% Fluid Structure Coupling

process = FSPC.Process()
solver = process.getSolver(pathF,pathS)
com = process.com

# Configure the algorithm

algorithm = FSPC.IQN_MVJ(solver,com)
algorithm.interp = FSPC.KNN(solver,1,com)
algorithm.converg = FSPC.Convergence(1e-8)
algorithm.step = FSPC.TimeStep(1e-3)

algorithm.endTime = 4
algorithm.omega = 0.5
algorithm.iterMax = 25
algorithm.dtWrite = 0.1

# Start the FSPC simulation

algorithm.simulate(com)
FSPC.printClock(com)