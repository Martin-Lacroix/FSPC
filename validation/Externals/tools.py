import numpy as np
import gmsh
import os

# %% Reads a Node Position

def readNode(index):

    gmsh.initialize()
    gmsh.option.setNumber('General.Terminal',0)

    # Lists the files and times

    name = [file for file in os.listdir() if('.msh' in file)]
    time = np.array([float(file[6:-4]) for file in name])
    coord = np.zeros((time.size,3))

    # Gets the nodal coordinates

    for i in range(len(name)):

        gmsh.open(name[i])
        coord[i] = gmsh.model.mesh.getNode(index)[0]

    # Correctly order the vectors

    index = np.argsort(time)
    coord = coord[index]
    time = time[index]

    gmsh.finalize()
    return time,coord-coord[0]

def readNode2(index):

    gmsh.initialize()
    gmsh.option.setNumber('General.Terminal',0)

    # Lists the files and times

    name = [file for file in os.listdir() if('.msh' in file)]
    time = np.array([float(file[6:-4]) for file in name])
    coord = np.zeros((time.size,3))

    # Gets the nodal coordinates

    for i in range(len(name)):

        gmsh.open(name[i])
        coord[i] = gmsh.model.mesh.getNode(index)[0]

    # Correctly order the vectors

    index = np.argsort(time)
    coord = coord[index]
    time = time[index]

    gmsh.finalize()
    return time,coord

# %% Find the Node Tag at Position

def getIndex(position):

    gmsh.initialize()
    gmsh.option.setNumber('General.Terminal',0)

    # Lists the files and times

    name = [file for file in os.listdir() if('.msh' in file)]
    time = np.array([float(file[6:-4]) for file in name])
    coord = np.zeros((time.size,3))

    # Find the closest node of position

    index = np.argmin(time)
    gmsh.open(name[index])

    tag,coord,_ = gmsh.model.mesh.getNodes()
    coord = np.array(np.split(coord,coord.size//3))

    dist = np.linalg.norm(position-coord,axis=1)
    index = np.argmin(dist)

    gmsh.finalize()
    return tag[index]