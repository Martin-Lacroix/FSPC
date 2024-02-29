import os.path as path
import numpy as np
import FSPC

# Input parameters for FSPC

R = 0.05
RBF = lambda r: np.square(r/R)*np.ma.log(r/R)
pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# Initialize the simulation

FSPC.setResMech(1e-6)
FSPC.setStep(1e-2,0.05)
FSPC.setSolver(pathF,pathS)
FSPC.setInterp(FSPC.interpolator.RBF,RBF)
FSPC.setAlgo(FSPC.algorithm.ILS,25)

# Start the FSPC simulation

FSPC.general.simulate(20)
FSPC.general.printClock()