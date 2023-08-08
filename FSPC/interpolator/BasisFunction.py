from .Interpolator import Interpolator
from ..general import Toolbox as tb
import numpy as np

# %% Mesh Interpolation with Radial Basis Functions

class RBF(Interpolator):
    def __init__(self,func):
        self.function = func

    # Compute the FS mesh interpolation matrix

    def initialize(self):

        Interpolator.__init__(self)
        position = tb.solver.getPosition()
        self.H = self.computeMapping(position)

# %% Mapping Matrix from RecvPos to Position

    @tb.compute_time
    def computeMapping(self,position):

        B = self.makeB(position)
        A = self.makeA()

        # Compute the interpolation H matrix

        H = np.transpose(np.linalg.lstsq(A,B,-1)[0])
        return H[np.ix_(range(self.nbrNode),range(self.recvNode))]

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
        B = np.ones((size,self.nbrNode))

        # Loop on the node positions in reference mesh

        for i,pos in enumerate(position):
            
            rad = np.linalg.norm(pos-self.recvPos,axis=1)
            B[range(self.recvNode),i] = self.function(rad)
            B[range(self.recvNode+1,size),i] = pos

        return B
