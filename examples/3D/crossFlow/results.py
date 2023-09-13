from matplotlib import pyplot as plt
import numpy as np
import gmsh
import os

# |------------------------------|
# |   Data From the Literature   |
# |------------------------------|

data = list()

# Bano Results

data.append(
[[0.00000,0.000000],
[0.024242,0.006306],
[0.044444,0.015855],
[0.062626,0.025765],
[0.076767,0.037297],
[0.092929,0.047387],
[0.117171,0.058378],
[0.139393,0.070090],
[0.169696,0.080180],
[0.208080,0.088828],
[0.258585,0.095495],
[0.327272,0.098558],
[0.389898,0.098198],
[0.462626,0.097657],
[0.535353,0.096216],
[0.632323,0.094774],
[0.741414,0.093693],
[0.868686,0.092792],
[1.000000,0.092252],
[1.185858,0.091891],
[1.381818,0.091351],
[1.503030,0.091351],
[1.717171,0.090990],
[1.854545,0.090990],
[2.002020,0.090990]])

# |-------------------------------|
# |   Post Procesing of Results   |
# |-------------------------------|

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
    coord[i] = gmsh.model.mesh.getNode(35)[0]

gmsh.finalize()
disp = np.linalg.norm(coord-coord[0],axis=1)
time = np.sort(time)

# Plot the final solution

for D in data: plt.plot(*np.transpose(D))
plt.plot(time,disp,'k--')
plt.grid()
plt.show()

