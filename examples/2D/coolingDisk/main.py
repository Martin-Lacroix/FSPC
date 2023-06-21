import os.path as path
import FSPC

# %% Input Parameters for FSPC

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# %% Initialize the Manager Module

FSPC.setStep(1e-2,0.01)
FSPC.setConvMecha(1e-8)
FSPC.setConvTherm(1e-6)
FSPC.setSolver(pathF,pathS)
FSPC.setInterp(FSPC.interpolator.KNN,2)

# Configure the algorithm

algorithm = FSPC.algorithm.ILS()
algorithm = FSPC.algorithm.MVJ()
algorithm.maxIter = 25
algorithm.endTime = 8
algorithm.omega = 0.5

# Start the FSPC simulation

algorithm.simulate()
FSPC.printClock()