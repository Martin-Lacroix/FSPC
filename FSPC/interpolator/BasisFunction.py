from .Interpolator import Interpolator
from ..general import Toolbox as tb
import numpy as np

# %% Mesh Interpolation Radial Basis Functions

class RBF(Interpolator):
    def __init__(self,func):
        self.function = func

    # Compute the FS mesh interpolation matrix

    def initialize(self):

        Interpolator.__init__(self)
        position = tb.solver.getPosition()
        self.computeMapping(position)

# %% Mapping Matrix from RecvPos to Position

    @tb.compute_time
    def computeMapping(self,position):

        self.B = self.makeB(position)
        self.A = self.makeA()

    # Interpolate RecvData and Return the Result

    @tb.compute_time
    def interpData(self,recvData):

        size = (tb.solver.dim+1,recvData.shape[1])
        result = np.append(recvData,np.zeros(size),axis=0)
        result = np.linalg.lstsq(self.A,result,-1)[0]
        return np.dot(self.B,result)

# %% Fill the A Matrix Using Basis Functions

    def makeA(self):

        size = 1+self.recvNode+tb.solver.dim
        A = np.zeros((size,size))

        # Loop on the node positions in target mesh

        for i,pos in enumerate(self.recvPos):

            A[self.recvNode,i] = 1
            A[i,self.recvNode] = 1

            A[range(1+self.recvNode,size),i] = pos
            A[i,range(1+self.recvNode,size)] = pos

            rad = np.linalg.norm(pos-self.recvPos,axis=1)
            A[range(self.recvNode),i] = self.function(rad)

        return A

# %% Fill the B Matrix Using Basis Functions

    def makeB(self,position):

        size = 1+self.recvNode+tb.solver.dim
        B = np.ones((self.nbrNode,size))

        # Loop on the node positions in reference mesh

        for i,pos in enumerate(position):
            
            rad = np.linalg.norm(pos-self.recvPos,axis=1)
            B[i,range(self.recvNode)] = self.function(rad)
            B[i,range(self.recvNode+1,size)] = pos

        return B
    