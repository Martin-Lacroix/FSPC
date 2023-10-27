import os.path as path
import numpy as np
import FSPC

# Input parameters for FSPC

R = 1e-2
RBF = lambda r: np.square(r/R)*np.ma.log(r/R)
pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# Initialize the simulation

FSPC.setConvMech(1e-6)
FSPC.setStep(5e-4,1e-3)
FSPC.setSolver(pathF,pathS)
FSPC.setInterp(FSPC.interpolator.RBF,RBF)
FSPC.setAlgo(FSPC.algorithm.MVJ,25)

# Start the FSPC simulation

FSPC.general.simulate(0.4)
FSPC.general.printClock()