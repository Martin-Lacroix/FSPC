from .Interpolator import Interpolator
from ..general import Toolbox as tb
import numpy as np

# %% Mesh Interpolation with K-Nearest Neighbours

class KNN(Interpolator):
    def __init__(self,K):
        Interpolator.__init__(self)

        # Compute the FS mesh interpolation matrix

        self.K = int(abs(K))
        position = tb.solver.getPosition()
        self.computeMapping(position)
        self.H = self.H.tocsr()

# %% Mapping Matrix from RecvPos to Position

    @tb.compute_time
    def computeMapping(self,pos):

        if self.K == 1: self.search(pos)
        else: self.interpolate(pos)

    # Nearest neighbour search if one neighbour

    def search(self,position):

        for i,pos in enumerate(position):

            dist = np.linalg.norm(pos-self.recvPos,axis=1)
            self.H[i,np.argmin(dist)] = 1

# %% Interpolate from the K nearest neighbours
 
    def interpolate(self,position):

        for i,pos in enumerate(position):

            dist = np.linalg.norm(pos-self.recvPos,axis=1)
            index = np.argsort(dist)[range(self.K)]
            weight = np.zeros(self.K)
            dist = dist[index]

            for j in range(self.K):

                val = [R for k,R in enumerate(dist) if k != j]
                weight[j] = np.prod(val)

            self.H[i,index] = weight/np.sum(weight)
