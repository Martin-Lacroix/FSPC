import os.path as path
import numpy as np
import FSPC

# Input Parameters for FSPC

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# |--------------------------------|
# |   Initialize the Simulation    |
# |--------------------------------|

R = 1e-2
RBF = lambda r: np.square(r/R)*np.ma.log(r/R)

FSPC.setConvMech(1e-6)
FSPC.setStep(5e-4,1e-3)
FSPC.setSolver(pathF,pathS)
FSPC.setInterp(FSPC.interpolator.RBF,RBF)

# Configure the algorithm

algorithm = FSPC.algorithm.MVJ()
algorithm.endTime = 0.4
algorithm.maxIter = 25
algorithm.omega = 0.5

# Start the FSPC simulation

algorithm.simulate()
FSPC.general.printClock()