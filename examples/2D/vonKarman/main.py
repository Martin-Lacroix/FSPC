from matplotlib import pyplot as plt
import os.path as path
import numpy as np
import FSPC
import sys


from interpolator import TEST

# %% Paths to the input files

pathF = path.dirname(__file__)+'/inputF.lua'
pathS = path.dirname(__file__)+'/inputS.py'

# %% Fluid Structure Coupling

process = FSPC.Process()
solver = process.getSolver(pathF,pathS)
RBF = lambda r: np.square(r)*np.ma.log(r)
initPos = solver.getPosition()

# Configure the algorithm

algorithm = FSPC.MVJ(solver)
algorithm.interp = FSPC.ETM(solver,4)
algorithm.convergM = FSPC.Convergence(1e-6)
algorithm.step = FSPC.TimeStep(1e-2,1e-2)

algorithm.endTime = 1
algorithm.omega = 0.5
algorithm.maxIter = 25

# Interpolation test class


algorithm.interp = TEST(solver,4)






# Start the FSPC simulation

algorithm.simulate()
FSPC.printClock()

# %% Get Curvilinear Indices

# %% Print the Results

# curvIdx,curvPos = algorithm.interp.makeCurvIndex()
# curvLoad,recvPos,recvLoad = algorithm.interp.getCurvLoad(curvIdx,curvPos)
# if process.com.rank == 1: sys.exit()

# color = dict()
# color['KNN'] = 'firebrick'
# color['RBF'] = 'darkorange'
# color['ETM'] = 'forestgreen'

# plt.figure(1)
# for key,val in recvLoad.items(): 
#     plt.plot(recvPos,val,'--',label=key,color=color[key])
#     plt.plot(recvPos,val,'.',markersize=7,color=color[key])

# for key,val in curvLoad.items(): plt.plot(curvPos,val,label=key,color='black')
# plt.legend()
# plt.grid()
# plt.show()
