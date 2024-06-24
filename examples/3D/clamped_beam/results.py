import os, sys
import numpy as np
sys.path.append('examples')
import toolbox as tb
import gmsh

# |-------------------------------|
# |   Data From the Literature    |
# |-------------------------------|

data = list()

# Results from Low

data.append([[0.00000, -8.7788e-7], [0.01000, -8.7788e-7]])

# Results from Ritz

data.append([[0.00000, -7.5922e-7], [0.01000, -7.5922e-7]])

# |--------------------------------|
# |   Post Procesing of Results    |
# |--------------------------------|

Z = list()
position = [0, 0, 0]
os.chdir('workspace/metafor')

time, directory = tb.read_files()
tag = tb.find_node(directory[0], position)

for file in directory:

    gmsh.open(file)
    Z.append(gmsh.model.mesh.getNode(tag)[0][2])

disp = Z-Z[0]
tb.plot_ref(time, disp, data)
