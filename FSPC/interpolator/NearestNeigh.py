from .Interpolator import Interpolator
from .. import Toolbox as tb
import numpy as np

# %% Mesh Interpolation with K-Nearest Neighbours

class KNN(Interpolator):
    def __init__(self,solver,K):
        Interpolator.__init__(self,solver)

        self.K = int(K)
        self.nbrNode = self.solver.nbrNode

        from scipy.sparse import dok_matrix
        self.H = dok_matrix((self.nbrNode,self.recvNode))

        # Compute the FS mesh interpolation matrix

        position = self.solver.getPosition()
        self.computeMapping(position)
        self.H = self.H.tocsr()

# %% Mapping Matrix from RecvPos to Position

    @tb.compute_time
    def computeMapping(self,pos):

        if self.K == 1: self.search(pos)
        else: self.interpolate(pos)

    # Nearest neighbour search if one neighbour

    def search(self,pos):

        for i in range(self.nbrNode):

            distance = np.linalg.norm(pos[i]-self.recvPos,axis=1)
            index = np.argmin(distance)
            self.H[i,index] = 1

    # Interpolate from the K nearest neighbours

    def interpolate(self,pos):

        for i in range(self.nbrNode):

            distance = np.linalg.norm(pos[i]-self.recvPos,axis=1)
            index = np.argsort(distance)[:self.K]
            weight = np.zeros(self.K)
            dist = distance[index]

            for j in range(self.K):

                val = [r for idx,r in enumerate(dist) if idx != j]
                weight[j] = np.prod(val)

            self.H[i,index] = weight/np.sum(weight)
