from matplotlib import pyplot as plt
import numpy as np
import gmsh
import os

# ----------------------------|
# Post Procesing of Results   |
# ----------------------------|

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
    coord[i] = gmsh.model.mesh.getNode(106)[0]

gmsh.finalize()
disp = (coord-coord[0])[:,1]
time = np.sort(time)

# Plot the final solution

plt.plot(time,disp,'k--')
plt.grid()
plt.show()