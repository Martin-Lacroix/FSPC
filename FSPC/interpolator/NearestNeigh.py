from .Interpolator import Interpolator
from scipy.sparse import dok_matrix
from ..toolbox import compute_time
from mpi4py import MPI
import numpy as np

# %% Mesh Interpolation with K-Nearest Neighbours

class KNN(Interpolator):
    def __init__(self,solver,K):
        Interpolator.__init__(self,solver)

        recvPos = None
        self.neigh = int(K)
        self.nbrNode = self.solver.nbrNode
        self.H = dok_matrix((self.nbrNode,self.recvNode),dtype=float)
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
        self.H = self.H.tocsr()

# %% Mapping Matrix from RecvPos to Position

    @compute_time
    def computeMapping(self,recvPos,position):

        if self.neigh == 1: self.search(recvPos,position)
        else: self.interp(recvPos,position)

    # Nearest neighbour search if one neighbour

    def search(self,recvPos,position):

        for i in range(self.nbrNode):

            distance = np.linalg.norm(position[i]-recvPos,axis=1)
            index = np.argmin(distance)
            self.H[i,index] = 1

    # Interpolate from the K nearest neighbours

    def interp(self,recvPos,position):

        for i in range(self.nbrNode):

            distance = np.linalg.norm(position[i]-recvPos,axis=1)
            index = np.argsort(distance)[:self.neigh]
            weight = np.zeros(self.neigh)
            dist = distance[index]

            for j in range(self.neigh):

                val = [r for idx,r in enumerate(dist) if idx != j]
                weight[j] = np.prod(val)

            self.H[i,index] = weight/np.sum(weight)
