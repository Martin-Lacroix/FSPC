from matplotlib import pyplot as plt
import numpy as np
import re,os
import gmsh

# |-------------------------------------------|
# |   Sort the Files in the Current Folder    |
# |-------------------------------------------|

def readFiles():

    time = list()
    directory = os.listdir()

    # Recover the time from the file name

    for F in directory:

        name = os.path.splitext(F)[0]
        T = float(re.compile(r'[^\d.]+').sub('',name))
        time.append(T)

    # Sort the list with respect to time

    time.sort()
    directory.sort()
    return time,directory

# |----------------------------------------------|
# |   Plot the Results and Reference Solution    |
# |----------------------------------------------|

def plotRef(time,result,reference):

    for R in reference: plt.plot(*np.transpose(R))

    # Plot my own results and compare with the reference

    plt.plot(time,result,'k--')
    plt.grid()
    plt.show()

# |---------------------------------------|
# |   Look For a Node in the Mesh File    |
# |---------------------------------------|

def findNode(file,position):

    gmsh.initialize()
    gmsh.option.setNumber('General.Terminal',0)
    gmsh.open(file)

    nodeTags,coord,_ = gmsh.model.mesh.getNodes()
    coord = coord.reshape(len(nodeTags),3)
    gmsh.clear()

    # Find the tag with minimum distance to position

    distance = np.linalg.norm(coord-position,axis=1)
    return int(nodeTags[np.argmin(distance)])