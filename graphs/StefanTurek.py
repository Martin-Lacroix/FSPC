from matplotlib import pyplot as plt
from Externals import tools
import numpy as np
import os

# %% Main Code

workspace = os.getcwd()
workspace += '/workspace/StefanTurek/metafor'
os.chdir(workspace)

# Reads the results

D = 0.1
time,disp = tools.readNode(657) # CHECK IF GOOD NODE !!!
results = [time,disp[:,1]]
disp = disp[:,1]

# Moves to main folder

workspace = os.path.split(workspace)[0]
os.chdir(workspace)

# %% Computation

zero = np.zeros(time.shape)
amplitude = (np.max(disp)-np.min(disp))/2
period = tools.interpolated_intercepts(time,zero,disp)[0]
period = period[-2]-period[-4]
strouhal = D/period[0]

# Relative amplitude and Strouhal

Turek = [0.83,0.19]
Fang_Bao = [0.78,0.19]
Bhardwaj = [0.92,0.19]

print('\nSolid Amplitude =',amplitude)
print('Strouhal Number =',strouhal,'\n')

# %% Save Results

plt.figure(1)
np.savetxt('output.dat',np.transpose(results),fmt=['%.6f','%.6f'])
plt.plot(*results)
plt.grid()
plt.show()