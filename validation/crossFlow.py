from matplotlib import pyplot as plt
from Externals import tools
from os import listdir
import numpy as np
import os

# %% Reads the Data

folder = os.getcwd()+'/validation/crossFlow/'
data = [np.loadtxt(folder+file).T for file in listdir(folder)]

# %% Print the Mass

workspace = os.getcwd()
workspace += '/workspace/crossFlow_3D'
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

tag = tools.getIndex([0.155,0.125,0.1])
time,disp = tools.readNode(tag)
results = [time,np.linalg.norm(disp,axis=1)]

# Moves to main folder

workspace = os.path.split(workspace)[0]
os.chdir(workspace)

# Save Results

plt.figure(2)
plt.gca().set_title('Output Data')
np.savetxt('output.dat',np.transpose(results),fmt=['%.6f','%.6f'])
plt.plot(*data[2])
plt.plot(*results,'k--')
plt.grid()
plt.show()

# %% Print the Output

workspace = os.getcwd()+'/metafor'
os.chdir(workspace)

# Reads the results
tag = np.array([
25,
841,
842,
843,
844,
845,
846,
847,
848,
849,
850,
851,
852,
853,
854,
855,
856,
857,
858,
859,
860,
861,
862,
863,
864,
865,
866,
867,
868,
869,
870,
871,
872,
873,
874,
875,
876,
877,
878,
45
],dtype=int)

Res = np.zeros((tag.size,2))
results = np.zeros((tag.size,3))

for i,T in enumerate(tag):

    print(T)
    time,coord = tools.readNode2(T)
    results[i] = coord[-1]

Res[:,0] = results[:,0]/0.1-1.5
Res[:,1] = results[:,2]/0.1

# Moves to main folder

workspace = os.path.split(workspace)[0]
os.chdir(workspace)

# Save Results

plt.figure(2)
plt.gca().set_title('Exp Data')
np.savetxt('profile.dat',Res,fmt=['%.6f','%.6f'])
plt.plot(*data[0])
plt.plot(*data[1])
plt.plot(*np.transpose(Res),'k--')
plt.grid()
plt.show()
