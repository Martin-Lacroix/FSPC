import os.path as path
import FSPC

# Input Parameters for FSPC

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# ----------------------------|
# Initialize the Simulation   |
# ----------------------------|

FSPC.setConvMech(1e-8)
FSPC.setStep(1e-3,1e-2)
FSPC.setSolver(pathF,pathS)
FSPC.setInterp(FSPC.interpolator.KNN,1)

# Configure the algorithm

algorithm = FSPC.algorithm.ILS()
algorithm.maxIter = 25
algorithm.endTime = 20
algorithm.omega = 0.5

# Start the FSPC simulation

algorithm.simulate()
FSPC.general.printClock()