from .Interpolator import Interpolator
from ..general import Toolbox as tb
from scipy import sparse as sp
import numpy as np

# %% Mesh Interpolation Element Transfer Method

class ETM(Interpolator):
    def __init__(self,K):
        self.K = int(abs(K))

    # Compute the FS mesh interpolation matrix

    def initialize(self):

        Interpolator.__init__(self)
        position = tb.solver.getPosition()
        self.computeMapping(position)
        self.H = self.H.tocsr()

    # Interpolate recvData and return the result

    @tb.compute_time
    def interpData(self,recvData):
        return self.H.dot(recvData)

# %% Mapping Matrix from RecvPos to Position

    @tb.compute_time
    def computeMapping(self,position):

        size = tb.solver.nbrNod,len(self.recvPos)
        self.H = sp.dok_matrix(size)

        # Loop on the node positions in reference mesh

        self.getFaceList()
        elem = tb.getElement(np.size(self.recvFace,1))
        faceList = self.getCloseFace(position)

        # Loop on the node positions in reference mesh

        for i,pos in enumerate(position):

            parList = list()
            disList = list()

            for j,k in enumerate(faceList[i]):

                node = self.recvPos[self.recvFace[k]]
                parList.append(elem.projection(node,pos))
                disList.append(elem.distance(parList[j],node,pos))

            # Store the closest projection in the H matrix

            idx = np.argmin(disList)
            face = self.recvFace[faceList[i][idx]]
            self.H[i,face] = elem.evaluate(parList[idx])

# %% Closest Facets to the Current Position

    def getCloseFace(self,position):
        
        result = np.zeros((tb.solver.nbrNod,self.K),int)
        facePos = np.mean(self.recvPos[self.recvFace],axis=1)

        for i,pos in enumerate(position):
            
            dist = np.linalg.norm(pos-facePos,axis=1)
            result[i] = np.argsort(dist)[range(self.K)]

        return result
