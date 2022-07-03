from matplotlib import pyplot as plt
from Externals import tools
import numpy as np
import os

# %% Main Code

workspace = os.getcwd()
workspace += '/workspace/GuiFourey/metafor'
os.chdir(workspace)

# Reads the results

time,disp = tools.readNode(106)
results = [time,disp[:,1]]
exact = -6.85e-5

# Moves to main folder

workspace = os.path.split(workspace)[0]
os.chdir(workspace)

# %% Save Results

plt.figure(1)
np.savetxt('output.dat',np.transpose(results),fmt=['%.6f','%.6f'])
plt.plot([0,time[-1]],[exact,exact])
plt.plot(*results,'k--')
plt.grid()
plt.show()