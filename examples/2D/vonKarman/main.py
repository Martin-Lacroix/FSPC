from matplotlib import pyplot as plt
import os.path as path
import numpy as np
import collections
import FSPC
import gmsh
import sys

# %% Paths to the input files

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# %% Fluid Structure Coupling

process = FSPC.Process()
solver = process.getSolver(pathF,pathS)
initPos = solver.getPosition()

# Configure the algorithm

algorithm = FSPC.MVJ(solver)
algorithm.interp = FSPC.KNN(solver,1)
algorithm.convergM = FSPC.Convergence(1e-6)
algorithm.step = FSPC.TimeStep(1e-2,1e-2)

algorithm.endTime = 1
algorithm.omega = 0.5
algorithm.maxIter = 25

# Start the FSPC simulation

algorithm.simulate()
FSPC.printClock()

# %% Post Processing Interpolation

if process.com.rank == 0:
    
    load = solver.getLoading()
    process.com.send(load.copy(),dest=1)
    mesh = path.dirname(__file__)+'/geometryF.msh'

if process.com.rank == 1:
    
    recvLoad = None
    mesh = path.dirname(__file__)+'/geometryS.msh'
    recvLoad = process.com.recv(recvLoad,source=0)
    load = algorithm.interp.interpData(recvLoad)

# Find the tag of FSInterface physical group

gmsh.initialize()
gmsh.open(mesh)

for data in gmsh.model.getPhysicalGroups():
    group = gmsh.model.getPhysicalName(*data)
    if group == 'FSInterface': physical = data

# Node with coordinates and elements of the interface

myDict = collections.defaultdict(list)
entity = gmsh.model.getEntitiesForPhysicalGroup(*physical)

for tag in entity:

    node,coord,param = gmsh.model.mesh.getNodes(1,tag,includeBoundary=True)
    coord = np.reshape(coord,(len(node),3))[:,:2]
    index = list(np.argsort(param))

    myDict['tags'] += node[index].tolist()
    myDict['coord'] += coord[index].tolist()

# Remove duplicate and keep the correct order

index = np.sort(np.unique(myDict['tags'],return_index=True)[1])
myDict['coord'] = np.array(myDict['coord'])[index]
myDict['tags'] = np.array(myDict['tags'])[index]

# Find the FSI indices along the parametric space

for i,coord in enumerate(myDict['coord']):

    dist = np.subtract(initPos,coord)
    index = np.argmin(np.linalg.norm(dist,axis=1))
    myDict['index'].append(index)

# get the loading from fluid solver

load = np.linalg.norm(load,axis=1)
load = load[myDict['index']]
gmsh.finalize()

# Make the curvilinear position vector

curvPos = np.zeros(solver.nbrNode)
position = initPos[myDict['index']]
diff = np.linalg.norm(np.diff(position,axis=0),axis=1)
for i in range(diff.size): curvPos[i+1] = curvPos[i]+diff[i]

# Send the solid data to the fluid

if process.com.rank == 0:
    
    recvLoad = None
    recvCurv = None
    recvLoad = process.com.recv(recvLoad,source=1)
    recvCurv = process.com.recv(recvCurv,source=1)

if process.com.rank == 1:

    process.com.send(load.copy(),dest=0)
    process.com.send(curvPos.copy(),dest=0)
    sys.exit()

# %% Print the Results

plt.figure(1)
plt.plot(curvPos,load,'--',label='Fluid')
plt.scatter(curvPos,load)
plt.plot(recvCurv,recvLoad,'--',label='Solid')
plt.scatter(recvCurv,recvLoad)
plt.grid()
plt.show()
