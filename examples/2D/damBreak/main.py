import os.path as path
import FSPC

# %% Input Parameters for FSPC

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

import numpy as np
RBF = lambda r: np.square(r)*np.ma.log(r)



print('\n\n',dir(FSPC),'\n\n')



# %% Initialize the Manager Module

FSPC.setStep(1e-3,1e-2)
FSPC.setConvMecha(1e-8)
FSPC.setSolver(pathF,pathS)
FSPC.setInterp(FSPC.RBF,RBF)

# Configure the algorithm

algorithm = FSPC.MVJ()
algorithm.maxIter = 25
algorithm.endTime = 1
algorithm.omega = 0.5

# Start the FSPC simulation

algorithm.simulate()
FSPC.printClock()