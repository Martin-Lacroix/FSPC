from scipy import interpolate
import os.path as path
from mpi4py import MPI
import numpy as np
import collections
import pickle
import FSPC
import gmsh

# %% Fluid Structure Coupling

class TEST(FSPC.ETM):
    def __init__(self,solver,K):
        FSPC.ETM.__init__(self,solver,K)
        
        RBF = lambda r: np.square(r)*np.ma.log(r)
        com = MPI.COMM_WORLD

        self.interp = dict()
        self.interp['ETM'] = FSPC.ETM(solver,9)
        self.interp['RBF'] = FSPC.RBF(solver,RBF)
        self.interp['KNN'] = FSPC.KNN(solver,2)

        self.error = dict()
        for key in self.interp.keys(): self.error[key] = list()
        solver.exit = self.printResult
        self.makeCurvIndex(com)

    def applyLoadFS(self,com):
        
        nbr = 1000
        error = dict()
        curvPos = np.linspace(0,max(self.curvPos),nbr)
        curvLoad,recvPos,recvLoad = self.getCurvLoad(com)

        if com.rank == 0:

            fun = interpolate.interp1d(self.curvPos,curvLoad['Fluid'],kind='linear')
            den = np.trapz(np.square(fun(curvPos)),curvPos)
            reference = fun(curvPos)

            for key,val in recvLoad.items():

                fun = interpolate.interp1d(recvPos,val,kind='linear')
                error = np.trapz(np.square(fun(curvPos)-reference),curvPos)
                self.error[key].append(error/den)

        return FSPC.ETM.applyLoadFS(self,com)

# %% Get Curvilinear Indices

    def makeCurvIndex(self,com):

        if com.rank == 0:
            mesh = path.dirname(__file__)+'/geometryF.msh'

        if com.rank == 1:
            mesh = path.dirname(__file__)+'/geometryS.msh'

        # Open the original mesh file
        
        gmsh.initialize()
        gmsh.open(mesh)

        for data in gmsh.model.getPhysicalGroups():
            group = gmsh.model.getPhysicalName(*data)
            if group == 'FSInterface': physical = data

        # Node with coordinates and elements of the interface

        initPos = self.solver.getPosition()
        myDict = collections.defaultdict(list)
        entity = gmsh.model.getEntitiesForPhysicalGroup(*physical)

        for tag in entity:

            node,coord,param = gmsh.model.mesh.getNodes(1,tag,includeBoundary=True)
            coord = np.reshape(coord,(len(node),3))[:,:2]
            index = list(np.argsort(param))

            myDict['tags'] += node[index].tolist()
            myDict['coord'] += coord[index].tolist()

        # Remove duplicate and keep the correct order

        index = np.sort(np.unique(myDict['tags'],return_index=True)[1])
        myDict['coord'] = np.array(myDict['coord'])[index]
        myDict['tags'] = np.array(myDict['tags'])[index]
        gmsh.finalize()

        # Find the curvilinear indices along the boundary

        for coord in myDict['coord']:

            dist = np.subtract(initPos,coord)
            index = np.argmin(np.linalg.norm(dist,axis=1))
            myDict['index'].append(index)

        # Compute the new curvilinear coordinates

        position = initPos[myDict['index']]
        self.curvPos = np.zeros(self.solver.nbrNode)
        diff = np.linalg.norm(np.diff(position,axis=0),axis=1)
        for i in range(diff.size): self.curvPos[i+1] = self.curvPos[i]+diff[i]
        self.curvIdx = myDict['index']

# %% Last Fluid-Solid Interpolation

    def getCurvLoad(self,com):

        recvPos = None
        curvLoad = dict()

        if com.rank == 0:

            curvLoad['Fluid'] = self.solver.getLoading()
            com.send(curvLoad['Fluid'],1,tag=11)

        if com.rank == 1:
            
            recvLoad = com.recv(source=0,tag=11) 
            for key in self.interp.keys(): 
                curvLoad[key] = self.interp[key].interpData(recvLoad)

        # Val[i] = stress tensor [xx,yy,xy]

        for key,val in curvLoad.items():
            curvLoad[key] = val[self.curvIdx,1]

        # Send the solid data to the fluid

        if com.rank == 0:

            recvLoad = dict()
            recvPos = com.recv(source=1,tag=12)
            for key in self.interp.keys():
                recvLoad[key] = com.recv(source=1,tag=13)

        if com.rank == 1:

            com.send(self.curvPos,0,tag=12)
            for key in self.interp.keys():
                com.send(curvLoad[key],0,tag=13)
        
        return curvLoad,recvPos,recvLoad

# %% Save the Current Result

    def printResult(self):

        out = dict()
        com = MPI.COMM_WORLD
        curvLoad,recvPos,recvLoad = self.getCurvLoad(com)

        if com.rank == 0:

            for key,val in self.error.items():
                self.error[key] = np.mean(val)
        
            # Save the result into a pickle

            out['recvPos'] = recvPos
            out['error'] = self.error
            out['recvLoad'] = recvLoad
            out['curvLoad'] = curvLoad
            out['curvPos'] = self.curvPos

            pickle.dump(out,open('out.pickle','wb'))
            