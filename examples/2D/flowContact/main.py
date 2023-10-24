import os.path as path
import FSPC

# Input parameters for FSPC

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# Initialize the simulation 

FSPC.setConvMech(1e-6)
FSPC.setStep(1e-4,1e-4)
FSPC.setSolver(pathF,pathS)
FSPC.setInterp(FSPC.interpolator.KNN,2)

# Configure the algorithm

algorithm = FSPC.algorithm.ILS()
algorithm.endTime = 0.05
algorithm.maxIter = 25
algorithm.omega = 0.5

# Start the FSPC simulation

algorithm.simulate()
FSPC.general.printClock()