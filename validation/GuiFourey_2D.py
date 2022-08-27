from matplotlib import pyplot as plt
from Externals import tools
import numpy as np
import os

# %% Print the Mass

workspace = os.getcwd()
workspace += '/workspace/GuiFourey_2D'
os.chdir(workspace)

# Reads the results

mass = np.loadtxt('mass.txt',delimiter=',').T
mass[1] = 100*mass[1]/mass[1,0]

# Save Results

plt.figure(1)
plt.gca().set_title('Total Mass')
np.savetxt('mass.dat',np.transpose(mass),fmt=['%.6f','%.6f'])
plt.plot(*mass)
plt.grid()
plt.show()

# %% Print the Output

workspace = os.getcwd()+'/metafor'
os.chdir(workspace)

# Reads the results

tag = tools.getIndex([0.5,0,0])
time,disp = tools.readNode(tag)
results = [time,disp[:,1]]
exact = -6.85e-5

# Moves to main folder

workspace = os.path.split(workspace)[0]
os.chdir(workspace)

# Save Results

plt.figure(2)
plt.gca().set_title('Output Data')
np.savetxt('output.dat',np.transpose(results),fmt=['%.6f','%.6f'])
plt.plot([0,time[-1]],[exact,exact])
plt.plot(*results,'k--')
plt.grid()
plt.show()