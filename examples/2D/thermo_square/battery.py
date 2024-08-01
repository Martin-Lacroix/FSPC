from matplotlib import pyplot as plt
from natsort import natsorted
import numpy as np
import os, gmsh

# Results from Long

plt.plot(*np.transpose(
[[0.00000, 2000.0000], [0.484928, 2000.0000], [1.048493, 2000.0000],
[1.612058, 2000.0000], [2.083879, 1998.2758], [2.542595, 1994.8275],
[2.948886, 1989.2241], [3.302752, 1983.6206], [3.643512, 1976.2931],
[4.062910, 1966.3793], [4.613368, 1951.7241], [5.058978, 1938.7931],
[5.517693, 1924.5689], [6.173001, 1905.1724], [6.736566, 1888.7931],
[7.260813, 1873.2758], [7.968545, 1853.4482], [8.414155, 1842.2413],
[8.846658, 1830.6034], [9.318480, 1819.3965], [9.750983, 1809.9137],
[10.00000, 1803.448]]))

# List the output files in workspace

gmsh.initialize()
gmsh.option.setNumber('General.Terminal', 0)
directory = natsorted(os.listdir('metafor'))

# Extract the results from Gmsh

time = list()
result = list()

for i, file in enumerate(directory):

    gmsh.open(f'metafor/{file}')

    time.append(float(file.replace('.msh', '').replace('output_', '')))
    temperature = gmsh.view.getModelData(2, i)[2][1400][0]+2000
    result.append(temperature)

# Plot the results on the graph

plt.grid(color='lightgray')
plt.plot(time, result, '--k')
plt.savefig('plot.pdf', format='pdf')
