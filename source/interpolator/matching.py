from .interpolator import Interpolator
from scipy.sparse import dok_matrix
import numpy as np

# %% Matching Meshes Interpolator

class Matching(Interpolator):
    def __init__(self,input,com):
        Interpolator.__init__(self,input,com)

        if self.nbrNode != self.recvNode:
            raise Exception('Different number of FSI nodes')

        # Initialize the FS interpolation matrix

        if com.rank == 0:
            
            self.H = dok_matrix((self.nbrNode,self.recvNode),dtype=int)
            positionS = np.zeros((self.recvNode,self.dim))
            positionF = self.solver.getPosition()
            com.Recv(positionS,source=1)

            # Compute H and send its transpose to Solid

            self.computeMappingF(positionS,positionF)
            com.send(self.H.transpose(),dest=1)
            self.H = self.H.tocsr()

        if com.rank == 1:
            
            self.H = None
            com.Send(self.solver.getPosition(),dest=0)
            self.H = com.recv(self.H,source=0)
            self.H = self.H.tocsr()

# %% Mapping matrix from Solid to Fluid

    def computeMappingF(self,positionS,positionF):

        for i in range(self.nbrNode):

            distance = np.linalg.norm(positionF[i]-positionS,axis=1)
            index = np.argmin(distance)
            self.H[i,index] = 1

    # Interpolate recvData and return the result

    def interpData(self,recvData):
        return self.H.dot(recvData)
