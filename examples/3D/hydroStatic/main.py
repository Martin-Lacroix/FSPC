import os.path as path
import FSPC

# Input parameters for FSPC

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# Initialize the simulation 

FSPC.setConvMech(1e-8)
FSPC.setStep(1e-2,0.05)
FSPC.setSolver(pathF,pathS)
FSPC.setInterp(FSPC.interpolator.ETM,9)

# Configure the algorithm

algorithm = FSPC.algorithm.ILS()
algorithm.maxIter = 25
algorithm.endTime = 20
algorithm.omega = 0.5

# Start the FSPC simulation

algorithm.simulate()
FSPC.general.printClock()