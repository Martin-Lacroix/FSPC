from matplotlib import pyplot as plt
from natsort import natsorted
import numpy as np
import os, gmsh

# Results from Low

plt.plot(*np.transpose(
[[0.00000, -8.7788e-7], [0.01000, -8.7788e-7]]))

# Results from Ritz

plt.plot(*np.transpose(
[[0.00000, -7.5922e-7], [0.01000, -7.5922e-7]]))

# List the output files in workspace

gmsh.initialize()
gmsh.option.setNumber('General.Terminal', 0)
directory = natsorted(os.listdir('metafor'))

# Extract the results from Gmsh

time = list()
result = list()

for file in directory:

    gmsh.open('metafor/'+file)

    time.append(float(file.replace('.msh', '').replace('output_', '')))
    distance = gmsh.model.mesh.getNode(1561)[0][2]
    result.append(distance)

# Plot the results on the graph

plt.grid(color='lightgray')
plt.plot(time, result, '--k')
plt.savefig('plot.pdf', format='pdf')
