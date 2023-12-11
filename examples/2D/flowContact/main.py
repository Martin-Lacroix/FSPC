import os.path as path
import FSPC

# Input parameters for FSPC

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# Initialize the simulation

FSPC.setConvMech(1e-4)
FSPC.setStep(1e-4,1e-4)
FSPC.setSolver(pathF,pathS)
FSPC.setInterp(FSPC.interpolator.KNN,1)
FSPC.setAlgo(FSPC.algorithm.MVJ,25)

# Start the FSPC simulation

FSPC.general.simulate(0.05)
FSPC.general.printClock()