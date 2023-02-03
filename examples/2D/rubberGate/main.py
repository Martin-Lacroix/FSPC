from matplotlib import pyplot as plt
import os.path as path
import numpy as np
import sys,os
import FSPC
import gmsh

# %% Paths to the input files

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# %% Fluid Structure Coupling

process = FSPC.Process()
solver = process.getSolver(pathF,pathS)

# Configure the algorithm

algorithm = FSPC.IQN_MVJ(solver)
algorithm.interp = FSPC.KNN(solver,2)
algorithm.convergM = FSPC.Convergence(1e-8)
algorithm.step = FSPC.TimeStep(5e-4)

algorithm.endTime = 0.4
algorithm.omega = 0.5
algorithm.maxIter = 25
algorithm.dtWrite = 1e-3

# Start the FSPC simulation

algorithm.simulate()
FSPC.printClock()

# %% Post Procesing of Results

if process.rank == 0: sys.exit()
if process.rank == 1: os.chdir('metafor')

gmsh.initialize()
gmsh.option.setNumber('General.Terminal',0)

# Extract the data from the mesh file

fileList = os.listdir()
time = [float(F[7:-4]) for F in fileList]
coord = np.zeros((len(fileList),3))
index = np.argsort(time)

for i,j in enumerate(index):

    gmsh.open(fileList[j])
    coord[i] = gmsh.model.mesh.getNode(124)[0]

gmsh.finalize()
disp = np.linalg.norm(coord-coord[0],axis=1)
time = np.sort(time)

# Plot the solid displacement

#for curve in data: plt.plot(*curve)
plt.plot(time,disp,'k--')
plt.grid()
plt.show()