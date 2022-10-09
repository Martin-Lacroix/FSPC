from .interpolator import Interpolator
from scipy.sparse import dok_matrix
import numpy as np

# %% Mesh Interpolation with Nearest Neighbour Search

class NNS(Interpolator):
    def __init__(self,input,com):
        Interpolator.__init__(self,input,com)

        recvPos = np.zeros((self.recvNode,self.dim))
        self.H = dok_matrix((self.nbrNode,self.recvNode),dtype=float)

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

    def computeMapping(self,recvPos,position):

        for i in range(self.nbrNode):

            distance = np.linalg.norm(position[i]-recvPos,axis=1)
            index = np.argsort(distance)[:2]

            totalDist = distance[index[0]]+distance[index[1]]
            self.H[i,index[0]] = distance[index[1]]/totalDist
            self.H[i,index[1]] = distance[index[0]]/totalDist

# %% Interpolate recvData and return the result

    def interpData(self,recvData):
        return self.H.dot(recvData)
