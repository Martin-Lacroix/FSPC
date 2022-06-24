from scipy.sparse import dok_matrix
from .tools import printY,Logs
from functools import reduce
import numpy as np

# %% Parent InterpolatorClass

class Interpolator(object):
    def __init__(self,input,param,com):

        printY('Initializing FSI Interpolator\n')

        self.com = com
        self.dim = param['dim']

        if com.rank == 0: self.solverF = input['solverF']
        if com.rank == 1: self.solverS = input['solverS']

        if com.rank == 0: self.nbrNode = self.solverF.nbrNode
        if com.rank == 1: self.nbrNode = self.solverS.nbrNode

        self.logForce = Logs('loads.log',['Time','Load'])

    def getLoadF(self):
        self.loadF = self.solverF.getLoading()

    def applyLoadS(self,time):
        
        self.solverS.applyLoading(self.loadS,time)
        load = np.linalg.norm(self.loadS.mean(axis=0))
        self.logForce.write(time,load)

    # Sets displacement to F solver
    
    def applyDispF(self,dt):
        self.solverF.applyDisplacement(self.dispF,dt)

    # Interpolation of [1] and store into [2] argument

    def interpLoadFS(self):

        if self.com.rank == 1: nbrNode = np.zeros(1,dtype=int)
        if self.com.rank == 0: self.com.Send(np.atleast_1d(self.nbrNode),dest=1)
        if self.com.rank == 1: self.com.Recv(nbrNode,source=0)

        if self.com.rank == 1: loadF = np.zeros((nbrNode[0],self.dim))
        if self.com.rank == 0: self.com.Send(self.loadF.copy(),dest=1)
        if self.com.rank == 1: self.com.Recv(loadF,source=0)

        if self.com.rank == 1: self.interpFS(loadF,self.loadS)

    def interpDispSF(self):

        if self.com.rank == 0: nbrNode = np.zeros(1,dtype=int)
        if self.com.rank == 1: self.com.Send(np.atleast_1d(self.nbrNode),dest=0)
        if self.com.rank == 0: self.com.Recv(nbrNode,source=1)

        if self.com.rank == 0: dispS = np.zeros((nbrNode[0],self.dim))
        if self.com.rank == 1: self.com.Send(self.dispS.copy(),dest=0)
        if self.com.rank == 0: self.com.Recv(dispS,source=1)

        if self.com.rank == 0: self.interpSF(dispS,self.dispF)

# %% Matching Meshes Interpolator

class Matching(Interpolator):
    def __init__(self,input,param,com):

        Interpolator.__init__(self,input,param,com)
        print('Setting matching mesh interpolator')

        if com.rank == 0: positionF = self.solverF.getPosition().T
        if com.rank == 1: positionS = self.solverS.getPosition().T

        if com.rank == 1: positionF = np.zeros((self.dim,self.nbrNode))
        if com.rank == 0: positionS = np.zeros((self.dim,self.nbrNode))

        if com.rank == 0: com.Send(positionF.copy(),dest=1)
        if com.rank == 1: com.Recv(positionF,source=0)

        if com.rank == 1: com.Send(positionS.copy(),dest=0)
        if com.rank == 0: com.Recv(positionS,source=1)

        self.makeInterfaceData()
        self.makeMapping(positionS,positionF)

    # Generates Interface Data
    
    def makeInterfaceData(self):

        if self.com.rank == 1: self.dispS = np.zeros((self.nbrNode,self.dim))
        if self.com.rank == 0: self.dispF = np.zeros((self.nbrNode,self.dim))
        if self.com.rank == 1: self.loadS = np.zeros((self.nbrNode,self.dim))
        if self.com.rank == 0: self.loadF = np.zeros((self.nbrNode,self.dim))

        self.H = dok_matrix((self.nbrNode,self.nbrNode),dtype=int)
        self.HT = dok_matrix((self.nbrNode,self.nbrNode),dtype=int)

    # Mapping between fluid and solid

    def makeMapping(self,positionS,positionF):

        print('Building interpolation matrix')

        location = [None]*self.dim
        
        for i in range(self.nbrNode):
            for j in range(self.dim):
                location[j] = np.where(np.isclose(positionF[j],positionS[j,i]))

            # Adds the position in the interpolation matrix

            idx = reduce(np.intersect1d,location)
            self.HT[i,idx] = 1
            self.H[idx,i] = 1

        self.HT.tocsr()
        self.H.tocsr()
        
    # Interpolation from fluid to solid

    def interpFS(self,dataF,dataS):

        for i in range(self.dim):
            dataS[:,i] = self.HT.dot(dataF[:,i])

    # Interpolation from solid to fluid

    def interpSF(self,dataS,dataF):

        for i in range(self.dim):
            dataF[:,i] = self.H.dot(dataS[:,i])
