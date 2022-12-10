from .interpolator import Interpolator
from scipy.sparse import dok_matrix
from ..toolbox import compute_time
import numpy as np

# %% Mesh Interpolation with Nearest Neighbour Search

class NNS(Interpolator):
    def __init__(self,solver,com):
        Interpolator.__init__(self,solver,com)

        recvPos = np.zeros((self.recvNode,self.dim))
        self.H = dok_matrix((self.nbrNode,self.recvNode),dtype=int)

        # Share the position vectors between solvers

        if com.rank == 0:

            com.Recv(recvPos,source=1)
            com.Send(self.solver.getPosition(),dest=1)

        if com.rank == 1:

            com.Send(self.solver.getPosition(),dest=0)
            com.Recv(recvPos,source=0)

        # Compute the FS mesh interpolation matrix

        position = self.solver.getPosition()
        self.computeMapping(recvPos,position)
        self.H = self.H.tocsr()

# %% Mapping matrix from Solid to Fluid

    @compute_time
    def computeMapping(self,recvPos,position):

        for i,pos in enumerate(position):

            distance = np.linalg.norm(pos-recvPos,axis=1)
            index = np.argmin(distance)
            self.H[i,index] = 1

# %% Interpolate recvData and return the result

    @compute_time
    def interpData(self,recvData):
        return self.H.dot(recvData)
