from matplotlib import pyplot as plt
from natsort import natsorted
import numpy as np
import os, gmsh

# Results from Onate

plt.plot(*np.transpose(
[[0.00000, 270.00000], [0.021288, 270.37594], [0.039301, 271.80451],
[0.065502, 276.09022], [0.094978, 282.63157], [0.124454, 290.15037],
[0.145742, 295.48872], [0.168668, 300.15037], [0.198144, 309.09774],
[0.234170, 315.63909], [0.319323, 321.95488], [0.350437, 322.48120],
[0.430677, 324.88721], [0.476528, 326.99248], [0.537118, 328.79699],
[0.617358, 331.72932], [0.753275, 333.15789], [0.921943, 335.33834],
[1.190502, 336.91729], [1.468886, 337.96992], [1.621179, 338.42105],
[1.996179, 338.87218], [2.457969, 339.24812], [2.996725, 339.62406]]))

# List the output files in workspace

gmsh.initialize()
gmsh.option.setNumber('General.Terminal', 0)
directory = natsorted(os.listdir('metafor'))

# Extract the results from Gmsh

time = list()
result = list()

for file in directory:

    gmsh.open(f'metafor/{file}')

    time.append(float(file.replace('.msh', '').replace('output_', '')))
    temperature = gmsh.view.getModelData(1, i)[2][628][0]+270
    result.append(temperature)

# Plot the results on the graph

plt.grid(color='lightgray')
plt.plot(time, result, '--k')
plt.savefig('plot.pdf', format='pdf')
