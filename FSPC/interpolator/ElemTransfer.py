from mpi4py.MPI import COMM_WORLD as CW
from ..general import ShapeFunction as sf
from .Interpolator import Interpolator
from ..general import Toolbox as tb
import numpy as np

# %% Mesh Interpolation with Element Transfer Method

class ETM(Interpolator):
    def __init__(self,K):
        Interpolator.__init__(self)

        # Share the facet vectors between solvers

        self.K = int(K)
        facet = tb.solver.getFacets()
        position = tb.solver.getPosition()

        if CW.rank == 0:
            
            CW.send(facet,1,tag=7)
            recvFacet = CW.recv(source=1,tag=8)

        if CW.rank == 1:

            recvFacet = CW.recv(source=0,tag=7)
            CW.send(facet,0,tag=8)

        # Compute the FS mesh interpolation matrix

        self.computeMapping(recvFacet,position)
        self.H = self.H.tocsr()

# %% Mapping Matrix from RecvPos to Position

    @tb.compute_time
    def computeMapping(self,recvFacet,pos):

        facetList = self.getCloseFacets(pos,recvFacet)

        if recvFacet.shape[1] == 2: fun = sf.Line()
        if recvFacet.shape[1] == 3: fun = sf.Triangle()
        if recvFacet.shape[1] == 4: fun = sf.Quadrangle()

        for i,node in enumerate(pos):

            parList = list()
            dist = np.zeros(facetList[i].size)

            for j,k in enumerate(facetList[i]):

                facetNodePos = self.recvPos[recvFacet[k]]
                param,dist[j] = fun.projection(facetNodePos,node)
                parList.append(param)

            # Store the closest projection in the H matrix

            idx = np.argmin(dist)
            facet = recvFacet[facetList[i][idx]]
            for j,k in enumerate(facet): self.H[i,k] = fun[j](parList[idx])

# %% Closest Facets to the Current Position

    def getCloseFacets(self,pos,recvFacet):
        
        result = np.zeros((tb.solver.nbrNode,self.K),int)

        for i,node in enumerate(pos):
            
            facetPosition = np.mean(self.recvPos[recvFacet],axis=1)
            dist = np.linalg.norm(node-facetPosition,axis=1)
            result[i] = np.argsort(dist)[:self.K]

        return result
