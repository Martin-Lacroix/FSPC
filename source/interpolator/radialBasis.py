from .interpolator import Interpolator
import numpy as np

# %% Mesh Interpolation with Radial Basis Functions

class RBF(Interpolator):
    def __init__(self,input,param,com):
        Interpolator.__init__(self,input,com)

        self.radius = param['radius']
        recvPos = np.zeros((self.recvNode,self.dim))
        self.function = getattr(self,'phi'+param['RBF'])

        # Compute the FS mesh interpolation matrix

        if com.rank == 0:

            com.Recv(recvPos,source=1)
            com.Send(self.solver.getPosition(),dest=1)

            position = self.solver.getPosition()
            self.computeMapping(recvPos,position)
            com.send(np.transpose(self.H),dest=1)

        if com.rank == 1:

            com.Send(self.solver.getPosition(),dest=0)
            com.Recv(recvPos,source=0)

            self.H = None
            self.H = com.recv(self.H,source=0)

# %% Mapping matrix from recvPos to position

    def computeMapping(self,recvPos,position):

        size = self.recvNode+self.dim+1
        B = np.ones((self.nbrNode,size))
        A = np.zeros((size,size))

        # Fill the matrices A,B with nodal positions

        B[:,self.recvNode+1:] = position
        A[:self.recvNode,self.recvNode+1:] = recvPos
        A[:self.recvNode,self.recvNode] = 1
        A += np.transpose(A)

        # Fill the matrices A,B using the basis function

        for i in range(self.recvNode):
            
            r = np.linalg.norm(recvPos[i]-recvPos,axis=1)
            A[i,:self.recvNode] = self.function(r/self.radius)

            r = np.linalg.norm(position-recvPos[i],axis=1)
            B[:,i] = self.function(r/self.radius)

        # Compute the interpolation H matrix

        self.H = np.linalg.solve(A.T,B.T).T
        self.H = self.H[:self.nbrNode,:self.recvNode]

# %% Interpolate recvData and return the result

    def interpData(self,recvData):
        return self.H.dot(recvData)

# %% Global Radial Basis Functions

    def phiVS(self,eps):
        return eps

    def phiTPS(self,eps):
        return (eps**2)*np.ma.log(eps)

    def phiMQ(self,eps):
        return np.sqrt(1+eps**2)

    def phiIMQ(self,eps):
        return 1/np.sqrt(1+eps**2)

    def phiIQ(self,eps):
        return 1/(1+eps**2)

    def phiGS(self,eps):
        return np.exp(-eps**2)

# %% Compact Radial Basis Functions

    def phiC0(self,eps):

        eps = eps.clip(max=1)
        return np.power(1-eps,2)

    def phiC2(self,eps):

        eps = eps.clip(max=1)
        return np.power(1-eps,4)*(4*eps+1)

    def phiC4(self,eps):

        eps = eps.clip(max=1)
        return np.power(1-eps,6)*(35*eps/3+6*eps+1)
