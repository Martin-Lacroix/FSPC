from ..ShapeFunction import Line,Triangle,Quadrangle
from .Interpolator import Interpolator
from scipy.sparse import dok_matrix
from ..Toolbox import compute_time
from mpi4py import MPI
import numpy as np

# %% Mesh Interpolation with Element Transfer Method

class ETM(Interpolator):
    def __init__(self,solver,K):
        Interpolator.__init__(self,solver)

        self.K = int(K)
        self.nbrNode = self.solver.nbrNode
        self.H = dok_matrix((self.nbrNode,self.recvNode),dtype=float)
        com = MPI.COMM_WORLD

        # Share the facet vectors between solvers

        facet = self.solver.getFacets()
        position = self.solver.getPosition()

        if com.rank == 0:
            
            com.send(facet,1,tag=7)
            recvFacet = com.recv(source=1,tag=8)

        if com.rank == 1:

            recvFacet = com.recv(source=0,tag=7)
            com.send(facet,0,tag=8)

        # Compute the FS mesh interpolation matrix

        self.computeMapping(recvFacet,position)
        self.H = self.H.tocsr()

# %% Mapping Matrix from RecvPos to Position

    @compute_time
    def computeMapping(self,recvFacet,pos):

        facetList = self.getCloseFacets(pos,recvFacet)

        if recvFacet.shape[1] == 2: fun = Line()
        if recvFacet.shape[1] == 3: fun = Triangle()
        if recvFacet.shape[1] == 4: fun = Quadrangle()

        for i,pos in enumerate(pos):

            parList = list()
            dist = np.zeros(facetList[i].size)

            for j,k in enumerate(facetList[i]):

                facetNodePos = self.recvPos[recvFacet[k]]
                param,dist[j] = fun.projection(facetNodePos,pos)
                parList.append(param)

            # Store the closest projection in the H matrix

            idx = np.argmin(dist)
            node = recvFacet[facetList[i][idx]]
            for j,k in enumerate(node): self.H[i,k] = fun[j](parList[idx])

# %% Closest Facets to the Current Position

    def getCloseFacets(self,pos,recvFacet):
        
        result = np.zeros((self.nbrNode,self.K),dtype=int)
        for i,node in enumerate(pos):
            
            facetPosition = np.mean(self.recvPos[recvFacet],axis=1)
            dist = np.linalg.norm(node-facetPosition,axis=1)
            result[i] = np.argsort(dist)[:self.K]

        return result
