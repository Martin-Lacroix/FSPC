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

    # Gets the vertical displacement

    for i in range(len(name)):

        gmsh.open(name[i])
        coord[i] = gmsh.model.mesh.getNode(index)[0]

    # Correctly order the vectors

    index = np.argsort(time)
    coord = coord[index]
    time = time[index]

    gmsh.finalize()
    return time,coord-coord[0]

#%% Intercept Function

def interpolated_intercepts(x,y1,y2):
    def intercept(point1,point2,point3,point4):
        def line(p1,p2):

            A = (p1[1]-p2[1])
            B = (p2[0]-p1[0])
            C = (p1[0]*p2[1]-p2[0]*p1[1])
            return A,B,-C

        def intersection(L1,L2):

            D  = L1[0]*L2[1]-L1[1]*L2[0]
            x = (L1[2]*L2[1]-L1[1]*L2[2])/D
            y = (L1[0]*L2[2]-L1[2]*L2[0])/D
            return x,y

        L1 = line([point1[0],point1[1]],[point2[0],point2[1]])
        L2 = line([point3[0],point3[1]],[point4[0],point4[1]])
        R = intersection(L1,L2)
        return R

    idxs = np.argwhere(np.diff(np.sign(y1-y2)) != 0)
    xcs = []
    ycs = []

    for idx in idxs:

        p1 = (x[idx],y1[idx])
        p2 = (x[idx+1],y1[idx+1])
        p3 = (x[idx],y2[idx])
        p4 = (x[idx+1],y2[idx+1])
        
        xc,yc = intercept(p1,p2,p3,p4)
        xcs.append(xc)
        ycs.append(yc)

    return np.array(xcs),np.array(ycs)