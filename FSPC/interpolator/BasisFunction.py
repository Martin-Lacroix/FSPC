from .Interpolator import Interpolator
from .. import Toolbox as tb
import numpy as np

# %% Mesh Interpolation with Radial Basis Functions

class RBF(Interpolator):
    def __init__(self,solver,fun):
        Interpolator.__init__(self,solver)

        self.function = fun
        self.nbrNode = self.solver.nbrNode

        # Compute the FS mesh interpolation matrix

        position = self.solver.getPosition()
        self.computeMapping(position)

# %% Mapping Matrix from RecvPos to Position

    @tb.compute_time
    def computeMapping(self,pos):

        size = self.recvNode+self.solver.dim+1
        B = np.ones((self.nbrNode,size))
        A = np.zeros((size,size))

        # Fill the matrices A,B with nodal positions

        B[:,self.recvNode+1:] = pos
        A[:self.recvNode,self.recvNode+1:] = self.recvPos
        A[:self.recvNode,self.recvNode] = 1
        A += np.transpose(A)

        # Fill the matrices A,B using the basis function

        for i,position in enumerate(self.recvPos):
            
            rad = np.linalg.norm(position-self.recvPos,axis=1)
            A[i,:self.recvNode] = self.function(rad)

            rad = np.linalg.norm(pos-position,axis=1)
            B[:,i] = self.function(rad)

        # Compute the interpolation H matrix

        try: self.H = np.linalg.lstsq(A.T,B.T,rcond=-1)[0].T
        except: self.H = np.linalg.solve(A.T,B.T).T
        self.H = self.H[:self.nbrNode,:self.recvNode]

