from .interpolator import Interpolator
from scipy import linalg
import numpy as np

# %% Energy Conservative Radial Basis Function

class EC_RBF(Interpolator):
    def __init__(self,input,com):
        Interpolator.__init__(self,input,com)

        # Initialize the FS interpolation matrix

        if com.rank == 0:

            positionS = np.zeros((self.recvNode,self.dim))
            positionF = self.solver.getPosition()
            com.Recv(positionS,source=1)

            # Compute A,B and send their transpose to Solid

            A = self.computeMappingF(positionS,positionF)
            com.send(np.transpose(self.B),dest=1)
            com.send(np.transpose(A),dest=1)
            self.LU = linalg.lu_factor(A)

        if com.rank == 1:

            A = None
            self.B = None
            com.Send(self.solver.getPosition(),dest=0)
            self.B = com.recv(self.B,source=0)

            # Precompute the LU decomposition for solve

            A = com.recv(A,source=0)
            self.LU = linalg.lu_factor(A)

# %% Mapping matrix from Solid to Fluid

    def computeMappingF(self,positionS,positionF):

        self.B = np.zeros((self.nbrNode,self.recvNode+self.dim+1))
        A = np.zeros((self.recvNode+self.dim+1,self.recvNode+self.dim+1))
        Cfs = np.zeros((self.nbrNode,self.recvNode))
        Css = np.zeros((self.recvNode,self.recvNode))
        Pf = np.ones((self.nbrNode,self.dim+1))
        Ps = np.ones((self.recvNode,self.dim+1))

        for i in range(self.recvNode):
            for j in range(self.recvNode):

                r = np.linalg.norm(positionS[i]-positionS[j])
                Css[i,j] = self.phiTPS(r)

        for i in range(self.nbrNode):
            for j in range(self.recvNode):

                r = np.linalg.norm(positionF[i]-positionS[j])
                Cfs[i,j] = self.phiTPS(r)

        Ps[:,1:] = positionS
        Pf[:,1:] = positionF

        self.B[:,0:self.recvNode] = Cfs
        self.B[:,self.recvNode:] = Pf

        A[:self.recvNode,:self.recvNode] = Css
        A[:self.recvNode,self.recvNode:] = Ps
        A[self.recvNode:,:self.recvNode] = Ps.T

        return A


# %% Interpolate recvData and return the result

    def interpDataSF(self,recvData):

            d = np.zeros((self.recvNode+self.dim+1,self.dim))
            d[:self.recvNode] = recvData

            test = linalg.lu_solve(self.LU,d)
            return self.B.dot(test)

    def interpDataFS(self,recvData):
            
            test = np.dot(self.B,recvData)
            t = linalg.lu_solve(self.LU,test)
            return t[:self.nbrNode]

# %% Thin Plate Spline Function

    def phiTPS(self,dist):

        if dist > 0: return (dist*dist)*np.log10(dist)
        else: return 0