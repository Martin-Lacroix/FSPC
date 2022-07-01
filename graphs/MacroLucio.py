from matplotlib import pyplot as plt
from Externals import tools
from os import listdir
import numpy as np
import os

# %% Reads the Data

folder = os.getcwd()+'/graphs/MarcoLucio/'
data = [np.loadtxt(folder+file).T for file in listdir(folder)]

# %% Main Code

workspace = os.getcwd()
workspace += '/workspace/MarcoLucio/metafor'
os.chdir(workspace)

# Reads the results

time,disp = tools.readNode(9)
results = [time,disp[:,0]]

# Moves to main folder

workspace = os.path.split(workspace)[0]
os.chdir(workspace)

# %% Save Results

plt.figure(1)
np.savetxt('output.dat',np.transpose(results),fmt=['%.6f','%.6f'])
for curve in data: plt.plot(*curve)
plt.plot(*results,'k--')
plt.grid()
plt.show()