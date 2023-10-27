import os.path as path
import FSPC

# Input parameters for FSPC

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# Initialize the simulation

FSPC.setConvTher(1e-8)
FSPC.setStep(1e-1,0.1)
FSPC.setSolver(pathF,pathS)
FSPC.setInterp(FSPC.interpolator.KNN,2)
FSPC.setAlgo(FSPC.algorithm.MVJ,25)

# Start the FSPC simulation

FSPC.general.simulate(20)
FSPC.general.printClock()