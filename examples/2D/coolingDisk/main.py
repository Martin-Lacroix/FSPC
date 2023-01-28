import os.path as path
import numpy as np
import FSPC
import os

# %% Paths to the input files

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# %% Fluid Structure Coupling

process = FSPC.Process()
solver = process.getSolver(pathF,pathS)

# Configure the algorithm

algorithm = FSPC.IQN_ILS(solver)
algorithm.interp = FSPC.KNN(solver,2)
algorithm.convergM = FSPC.Convergence(1e-8)
algorithm.convergT = FSPC.Convergence(1e-8)
algorithm.step = FSPC.TimeStep(1e-2)

algorithm.endTime = 20
algorithm.omega = 0.5
algorithm.maxIter = 25
algorithm.dtWrite = 0.01

# Start the FSPC simulation

algorithm.simulate()
FSPC.printClock()

# %% Post Procesing of Outputs

if process.rank == 0: os.chdir('pfem')
if process.rank == 1: os.chdir('metafor')

fileList = os.listdir()
time = [float(F[7:-4]) for F in fileList]

for i,j in enumerate(np.argsort(time)):

    output = 'output_'+str(i)+'.vtu'
    os.rename(fileList[j],output)