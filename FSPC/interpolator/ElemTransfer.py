from .Interpolator import Interpolator
from ..general import Toolbox as tb
from ..general import Element as el
import numpy as np

# %% Mesh Interpolation with Element Transfer Method

class ETM(Interpolator):
    def __init__(self,K):
        Interpolator.__init__(self)

        # Share the facet vectors between solvers

        self.K = int(abs(K))
        recvFacet = self.getFacets()
        position = tb.solver.getPosition()

        # Compute the FS mesh interpolation matrix

        self.computeMapping(position,recvFacet)
        self.H = self.H.tocsr()

# %% Mapping Matrix from RecvPos to Position

    @tb.compute_time
    def computeMapping(self,pos,recvFacet):

        E = self.getElement(recvFacet)
        facetList = self.getCloseFacets(pos,recvFacet)

        # Loop on the node positions in reference mesh

        for i,node in enumerate(pos):

            parList = list()
            dist = np.zeros(len(facetList[i]))

            for j,k in enumerate(facetList[i]):

                facetNodePos = self.recvPos[recvFacet[k]]
                param,dist[j] = E.projection(facetNodePos,node)
                parList.append(param)

            # Store the closest projection in the H matrix

            idx = np.argmin(dist)
            F = recvFacet[facetList[i][idx]]
            for j,k in enumerate(F): self.H[i,k] = E[j](parList[idx])

# %% Closest Facets to the Current Position

    def getCloseFacets(self,pos,recvFacet):
        
        result = np.zeros((self.nbrNode,self.K),int)

        for i,node in enumerate(pos):
            
            facetPosition = np.mean(self.recvPos[recvFacet],axis=1)
            dist = np.linalg.norm(node-facetPosition,axis=1)
            result[i] = np.argsort(dist)[range(self.K)]

        return result

# %% Return the Correct Shape Function Class

    def getElement(self,recvFacet):

        if np.size(recvFacet,1) == 2: return el.Line()
        if np.size(recvFacet,1) == 3: return el.Triangle()
        if np.size(recvFacet,1) == 4: return el.Quadrangle()
        raise Exception('Element type not yet supported')
