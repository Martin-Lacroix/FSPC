import os, sys
import numpy as np
sys.path.append('examples')
import toolbox as tb
import gmsh

# |-------------------------------|
# |   Data From the Literature    |
# |-------------------------------|

data = list()

# Bano results

data.append(
[[0.00000, 0.000000],
[0.024242, 0.006306],
[0.044444, 0.015855],
[0.062626, 0.025765],
[0.076767, 0.037297],
[0.092929, 0.047387],
[0.117171, 0.058378],
[0.139393, 0.070090],
[0.169696, 0.080180],
[0.208080, 0.088828],
[0.258585, 0.095495],
[0.327272, 0.098558],
[0.389898, 0.098198],
[0.462626, 0.097657],
[0.535353, 0.096216],
[0.632323, 0.094774],
[0.741414, 0.093693],
[0.868686, 0.092792],
[1.000000, 0.092252],
[1.185858, 0.091891],
[1.381818, 0.091351],
[1.503030, 0.091351],
[1.717171, 0.090990],
[1.854545, 0.090990],
[2.002020, 0.090990]])

# |--------------------------------|
# |   Post Procesing of Results    |
# |--------------------------------|

D = list()
position = [0.15, 0.125, 0.1]
os.chdir('workspace/metafor')

time, directory = tb.read_files()
tag = tb.find_node(directory[0], position)

for file in directory:

    gmsh.open(file)
    D.append(gmsh.model.mesh.getNode(tag)[0])

disp = np.linalg.norm(D - D[0], axis=1)
tb.plot_ref(time, disp, data)
