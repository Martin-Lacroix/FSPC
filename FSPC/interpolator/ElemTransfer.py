from .Interpolator import Interpolator
from ..general import Toolbox as tb
from ..general import Element as el
import numpy as np

# %% Mesh Interpolation with Element Transfer Method

class ETM(Interpolator):
    def __init__(self,K):
        Interpolator.__init__(self)

        # Share the facet vectors between solvers

        self.getFace()
        self.K = int(abs(K))
        position = tb.solver.getPosition()

        # Compute the FS mesh interpolation matrix

        self.computeMapping(position)
        self.H = self.H.tocsr()

# %% Mapping Matrix from RecvPos to Position

    @tb.compute_time
    def computeMapping(self,pos):

        E = self.getElement()
        faceList = self.getCloseFace(pos)

        # Loop on the node positions in reference mesh

        for i,nodePos in enumerate(pos):

            parm = list()
            dist = list()

            for j,k in enumerate(faceList[i]):

                facePos = self.recvPos[self.recvFace[k]]
                parm.append(E.projection(facePos,nodePos))
                dist.append(E.distance(parm[j],facePos,nodePos))

            # Store the closest projection in the H matrix

            D = np.argmin(dist)
            F = self.recvFace[faceList[i][D]]
            for j,k in enumerate(F): self.H[i,k] = E.N[j](parm[D])

# %% Closest Facets to the Current Position

    def getCloseFace(self,pos):
        
        result = np.zeros((self.nbrNode,self.K),int)
        facePos = np.mean(self.recvPos[self.recvFace],axis=1)

        for i,node in enumerate(pos):
            
            dist = np.linalg.norm(node-facePos,axis=1)
            result[i] = np.argsort(dist)[range(self.K)]

        return result

# %% Return the Correct Shape Function Class

    def getElement(self):

        if np.size(self.recvFace,1) == 2: return el.Line()
        if np.size(self.recvFace,1) == 3: return el.Triangle()
        if np.size(self.recvFace,1) == 4: return el.Quadrangle()
        raise Exception('Element type not yet supported')
