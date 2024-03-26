from matplotlib import pyplot as plt
import numpy as np
import re, os
import gmsh

# |---------------------------------------|
# |   Sort the Files in Current Folder    |
# |---------------------------------------|

def read_files():

    time = list()
    directory = np.array(os.listdir())

    # Recover the time from the file name

    for F in directory:

        name = os.path.splitext(F)[0]
        T = float(re.compile(r'[^\d.]+').sub('', name))
        time.append(T)

    # Sort the list with respect to time

    IDX = np.argsort(time)
    time = np.array(time)[IDX]
    return time, directory[IDX]

# |-------------------------------------|
# |   Plot the Results and Reference    |
# |-------------------------------------|

def plot_ref(time: list, result: list, reference: list):

    result = np.atleast_2d(result)
    for R in reference: plt.plot(*np.transpose(R))
    for R in result: plt.plot(time, R, 'k--')
    plt.grid()
    plt.show()

# |---------------------------------------|
# |   Look For a Node in the Mesh File    |
# |---------------------------------------|

def find_node(file: str, position: np.ndarray):

    gmsh.initialize()
    gmsh.option.setNumber('General.Terminal', 0)
    gmsh.open(file)

    node_tags, coord, _ = gmsh.model.mesh.getNodes()
    coord = coord.reshape(len(node_tags), 3)
    gmsh.clear()

    # Find the tag with minimum distance to position

    distance = np.linalg.norm(coord-position, axis=1)
    return int(node_tags[np.argmin(distance)])