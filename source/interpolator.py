from scipy.sparse import dok_matrix
from .tools import printY,scatterFS,scatterSF
from functools import reduce
import numpy as np

# %% Parent InterpolatorClass

class Interpolator(object):
    def __init__(self,input,param,com):

        printY('Initializing FSI Interpolator\n')

        self.dim = param['dim']
        self.solver = input['solver']
        self.nbrNode = self.solver.nbrNode

    # Apply and get data from solid and fluid solvers

    def getLoadF(self):
        self.load = self.solver.getLoading()

    def applyLoadS(self,time):
        self.solver.applyLoading(self.load,time)
    
    def applyDispF(self,dt):
        self.solver.applyDisplacement(self.disp,dt)

    # Loading interpolation from fluid to solid

    def interpLoadFS(self,com):

        nbrNode = scatterFS(self.nbrNode,com)

        if com.rank == 1: load = np.zeros((nbrNode,self.dim))
        if com.rank == 0: com.Send(self.load.copy(),dest=1)

        if com.rank == 1: com.Recv(load,source=0)
        if com.rank == 1: self.load = self.interpData(load)

    # Displacement interpolation from solid to fluid

    def interpDispSF(self,com):

        nbrNode = scatterSF(self.nbrNode,com)

        if com.rank == 0: disp = np.zeros((nbrNode,self.dim))
        if com.rank == 1: com.Send(self.disp.copy(),dest=0)

        if com.rank == 0: com.Recv(disp,source=1)
        if com.rank == 0: self.disp = self.interpData(disp)

# %% Matching Meshes Interpolator

class Matching(Interpolator):
    def __init__(self,input,param,com):

        Interpolator.__init__(self,input,param,com)
        print('Setting matching mesh interpolator')

        nbrNode = scatterSF(self.nbrNode,com)
        input = np.zeros((self.dim,nbrNode))
        output = self.solver.getPosition().T

        if com.rank == 0: com.Send(output.copy(),dest=1)
        if com.rank == 1: com.Recv(input,source=0)

        if com.rank == 1: com.Send(output.copy(),dest=0)
        if com.rank == 0: com.Recv(input,source=1)

        self.makeInterfaceData()
        self.makeMapping(input,output)
        self.H = self.H.tocsr()

    # Generates initial interface data
    
    def makeInterfaceData(self):

        self.disp = np.zeros((self.nbrNode,self.dim))
        self.load = np.zeros((self.nbrNode,self.dim))
        self.H = dok_matrix((self.nbrNode,self.nbrNode),dtype=int)

    # Mapping matrix from input to output nodes

    def makeMapping(self,input,output):

        print('Building interpolation matrix')
        find = lambda F,S : np.where(np.isclose(F,S))
        
        for i in range(self.nbrNode):
            
            loc = [find(output[j],input[j,i]) for j in range(self.dim)]
            index = reduce(np.intersect1d,loc)
            self.H[index,i] = 1

    # Interpolation from input to output nodal data

    def interpData(self,inputData):
        return self.H.dot(inputData)
