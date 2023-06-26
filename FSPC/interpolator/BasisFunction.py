from .Interpolator import Interpolator
from ..general import Toolbox as tb
import numpy as np

# %% Mesh Interpolation with Radial Basis Functions

class RBF(Interpolator):
    def __init__(self,func):
        Interpolator.__init__(self)

        # Compute the FS mesh interpolation matrix

        self.function = func
        position = tb.solver.getPosition()
        self.H = self.computeMapping(position)

# %% Mapping Matrix from RecvPos to Position

    @tb.compute_time
    def computeMapping(self,pos):

        size = 1+self.recvNode+tb.solver.dim
        B = np.ones((size,self.nbrNode))
        A = np.zeros((size,size))

        # Fill the B matrix using the basis function

        for i,position in enumerate(pos):
            
            rad = np.linalg.norm(position-self.recvPos,axis=1)
            B[range(self.recvNode),i] = self.function(rad)
            B[range(self.recvNode+1,size),i] = position

        # Fill the A matrix using the basis function

        for i,recvPos in enumerate(self.recvPos):

            A[self.recvNode,i] = 1
            A[i,self.recvNode] = 1

            A[range(self.recvNode+1,size),i] = recvPos
            A[i,range(self.recvNode+1,size)] = recvPos

            rad = np.linalg.norm(recvPos-self.recvPos,axis=1)
            A[range(self.recvNode),i] = self.function(rad)

        # Compute the interpolation H matrix

        try: H = np.transpose(np.linalg.lstsq(A,B,-1)[0])
        except: H = np.transpose(np.linalg.solve(A,B))
        return H[np.ix_(range(self.nbrNode),range(self.recvNode))]
