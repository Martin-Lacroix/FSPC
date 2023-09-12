import os.path as path
import FSPC

# Input Parameters for FSPC

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# ----------------------------|
# Initialize the Simulation   |
# ----------------------------|

FSPC.setConvMech(1e-8)
FSPC.setConvTher(1e-6)
FSPC.setStep(1e-3,0.01)
FSPC.setSolver(pathF,pathS)
FSPC.setInterp(FSPC.interpolator.ETM,9)


# Configure the algorithm

algorithm = FSPC.algorithm.MVJ()
algorithm.maxIter = 25
algorithm.endTime = 3
algorithm.omega = 0.5

# Start the FSPC simulation

algorithm.simulate()
FSPC.general.printClock()