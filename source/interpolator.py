from scipy.sparse import dok_matrix
from .tools import printY,Logs,scatterFS,scatterSF
from functools import reduce
import numpy as np

# %% Parent InterpolatorClass

class Interpolator(object):
    def __init__(self,input,param,com):

        printY('Initializing FSI Interpolator\n')

        self.dim = param['dim']

        if com.rank == 0: self.solverF = input['solverF']
        if com.rank == 1: self.solverS = input['solverS']

        if com.rank == 0: self.nbrNode = self.solverF.nbrNode
        if com.rank == 1: self.nbrNode = self.solverS.nbrNode

        self.logForce = Logs('loads.log',['Time','Load'])

    # Apply and get data from solid and fluid solvers

    def getLoadF(self):
        self.loadF = self.solverF.getLoading()

    def applyLoadS(self,time):
        
        self.solverS.applyLoading(self.loadS,time)
        load = np.linalg.norm(self.loadS.mean(axis=0))
        self.logForce.write(time,load)
    
    def applyDispF(self,dt):
        self.solverF.applyDisplacement(self.dispF,dt)

    # Loading interpolation from fluid to solid

    def interpLoadFS(self,com):

        nbrNode = scatterFS(self.nbrNode,com)
        if com.rank == 0: com.Send(self.loadF.copy(),dest=1)
        else:

            loadF = np.zeros((nbrNode,self.dim))
            com.Recv(loadF,source=0)
            self.interpData(loadF,self.loadS)

    # Displacement interpolation from solid to fluid

    def interpDispSF(self,com):

        nbrNode = scatterSF(self.nbrNode,com)
        if com.rank == 1: com.Send(self.dispS.copy(),dest=0)
        else:

            dispS = np.zeros((nbrNode,self.dim))
            com.Recv(dispS,source=1)
            self.interpData(dispS,self.dispF)

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

        self.makeInterfaceData(com)
        self.makeMapping(positionS,positionF)
        if com.rank == 1: self.H = self.H.transpose()
        self.H = self.H.tocsr()

    # Generates Interface Data
    
    def makeInterfaceData(self,com):

        if com.rank == 0: self.dispF = np.zeros((self.nbrNode,self.dim))
        if com.rank == 0: self.loadF = np.zeros((self.nbrNode,self.dim))

        if com.rank == 1: self.dispS = np.zeros((self.nbrNode,self.dim))
        if com.rank == 1: self.loadS = np.zeros((self.nbrNode,self.dim))
        
        self.H = dok_matrix((self.nbrNode,self.nbrNode),dtype=int)

    # Mapping between fluid and solid

    def makeMapping(self,positionS,positionF):

        print('Building interpolation matrix')
        find = lambda F,S : np.where(np.isclose(F,S))
        
        for i in range(self.nbrNode):
            
            loc = [find(positionF[j],positionS[j,i]) for j in range(self.dim)]
            index = reduce(np.intersect1d,loc)
            self.H[index,i] = 1

    # Interpolation of nodal data from input to output

    def interpData(self,input,output):

        for i in range(self.dim):
            output[:,i] = self.H.dot(input[:,i])
