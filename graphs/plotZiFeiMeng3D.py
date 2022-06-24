from matplotlib import pyplot as plt
from Externals import tools
from os import listdir
import numpy as np
import os

# %% Reads the Data

folder = os.getcwd()+'/graphs/ZiFeiMeng/'
data = [np.loadtxt(folder+file).T for file in listdir(folder)]

# %% Main Code

workspace = os.getcwd()
workspace += '/workspace/ZiFeiMeng3D/metafor'
os.chdir(workspace)

# Reads the results

time,disp = tools.readNode(1231)
resultsX = [time,disp[:,0]]
resultsY = [time,disp[:,2]]

# Moves to main folder

workspace = os.path.split(workspace)[0]
os.chdir(workspace)

# %% Save Results

plt.figure(1)
np.savetxt('output.dat',np.transpose(resultsX),fmt=['%.6f','%.6f'])
np.savetxt('output.dat',np.transpose(resultsY),fmt=['%.6f','%.6f'])
for curve in data: plt.plot(*curve)
plt.plot(*resultsX,'k--')
plt.plot(*resultsY,'k--')
plt.grid()
plt.show()