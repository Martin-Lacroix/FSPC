from matplotlib import pyplot as plt
import numpy as np
import gmsh
import os

# %% Post Procesing of Results

gmsh.initialize()
gmsh.option.setNumber('General.Terminal',0)
os.chdir('workspace/metafor')

# Extract the data from the mesh file

fileList = os.listdir()
time = [float(F[7:-4]) for F in fileList]
coord = np.zeros((len(fileList),3))
index = np.argsort(time)

for i,j in enumerate(index):

    gmsh.open(fileList[j])
    coord[i] = gmsh.model.mesh.getNode(79)[0]

gmsh.finalize()
disp = (coord-coord[0])[:,1]
time = np.sort(time)

# Relative amplitude and frequency

fourier = np.fft.fft(disp)[range(len(disp)//2)]
freq = np.arange(len(disp)//2)/time[-1]

F = freq[np.argmax(abs(fourier))]
A = (np.max(disp)-np.min(disp))/2

# Plot the solid displacement

print('\nAmplitude : {:.6f}'.format(A))
print('Frequency : {:.6f}\n'.format(F))

plt.plot(time,disp,'k')
plt.grid()
plt.show()
