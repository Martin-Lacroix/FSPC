from .Interpolator import Interpolator
from ..general import Toolbox as tb
from scipy import sparse as sp
import numpy as np

# %% Mesh Interpolation K-Nearest Neighbours

class KNN(Interpolator):
    def __init__(self,K):
        self.K = int(abs(K))

    # Compute the FS mesh interpolation matrix

    def initialize(self):

        Interpolator.__init__(self)
        self.H = sp.dok_matrix((self.nbrNode,self.recvNode))
        position = tb.solver.getPosition()
        self.computeMapping(position)
        self.H = self.H.tocsr()

# %% Mapping Matrix from RecvPos to Position

    @tb.compute_time
    def computeMapping(self,position):

        if self.K == 1: self.search(position)
        else: self.interpolate(position)

    # Interpolate RecvData and Return the Result

    @tb.compute_time
    def interpData(self,recvData):
        return self.H.dot(recvData)

# %% Find the K Nearest Neighbours
 
    def search(self,position):

        for i,pos in enumerate(position):

            dist = np.linalg.norm(pos-self.recvPos,axis=1)
            self.H[i,np.argmin(dist)] = 1

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
