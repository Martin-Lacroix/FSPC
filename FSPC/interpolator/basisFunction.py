from .Interpolator import Interpolator
from ..toolbox import compute_time
from mpi4py import MPI
import numpy as np

# %% Mesh Interpolation with Radial Basis Functions

class RBF(Interpolator):
    def __init__(self,solver,fun):
        Interpolator.__init__(self,solver)

        recvPos = None
        self.function = fun
        self.nbrNode = self.solver.nbrNode
        com = MPI.COMM_WORLD

        # Share the position vectors between solvers

        if com.rank == 0:

            recvPos = com.recv(recvPos,source=1)
            com.send(self.solver.getPosition(),dest=1)

        if com.rank == 1:

            com.send(self.solver.getPosition(),dest=0)
            recvPos = com.recv(recvPos,source=0)

        # Compute the FS mesh interpolation matrix

        position = self.solver.getPosition()
        self.computeMapping(recvPos,position)


# %% Mapping Matrix from RecvPos to Position

    @compute_time
    def computeMapping(self,recvPos,position):

        size = self.recvNode+self.solver.dim+1
        B = np.ones((self.nbrNode,size))
        A = np.zeros((size,size))

        # Fill the matrices A,B with nodal positions

        B[:,self.recvNode+1:] = position
        A[:self.recvNode,self.recvNode+1:] = recvPos
        A[:self.recvNode,self.recvNode] = 1
        A += np.transpose(A)

        # Fill the matrices A,B using the basis function

        for i,pos in enumerate(recvPos):
            
            rad = np.linalg.norm(pos-recvPos,axis=1)
            A[i,:self.recvNode] = self.function(rad)

            rad = np.linalg.norm(position-pos,axis=1)
            B[:,i] = self.function(rad)

        # Compute the interpolation H matrix

        try: self.H = np.linalg.lstsq(A.T,B.T,rcond=-1)[0].T
        except: self.H = np.linalg.solve(A.T,B.T).T
        self.H = self.H[:self.nbrNode,:self.recvNode]
