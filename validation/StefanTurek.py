from matplotlib import pyplot as plt
from Externals import tools
import numpy as np
import os

# %% Print the Mass

workspace = os.getcwd()
workspace += '/workspace/StefanTurek'
os.chdir(workspace)

# Reads the results

mass = np.loadtxt('mass.txt',delimiter=',').T
mass[1] = 100*mass[1]/mass[1,0]

# Save Results

plt.figure(1)
np.savetxt('mass.dat',np.transpose(mass),fmt=['%.6f','%.6f'])
plt.plot(*mass)
plt.grid()
plt.show()

# %% Print the Output

workspace = os.getcwd()+'/metafor'
os.chdir(workspace)

# Reads the results

D = 0.1
time,disp = tools.readNode(657) # CHECK IF GOOD NODE !!!
results = [time,disp[:,1]]
disp = disp[:,1]

# Moves to main folder

workspace = os.path.split(workspace)[0]
os.chdir(workspace)

# Relative amplitude and Strouhal

zero = np.zeros(time.shape)
amplitude = (np.max(disp)-np.min(disp))/2
period = tools.interpolated_intercepts(time,zero,disp)[0]
period = period[-2]-period[-4]
strouhal = D/period[0]

print('Solid Amplitude =',amplitude)
print('Strouhal Number =',strouhal)

# %% Save Results

plt.figure(1)
np.savetxt('output.dat',np.transpose(results),fmt=['%.6f','%.6f'])
plt.plot(*results)
plt.grid()
plt.show()