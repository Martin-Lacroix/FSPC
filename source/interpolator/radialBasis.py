from .interpolator import Interpolator
from scipy import linalg
import numpy as np

# %% Matching Meshes Interpolator

class EC_RBF(Interpolator):
    def __init__(self,input,com):
        Interpolator.__init__(self,input,com)

        # Initialize the FS interpolation matrix

        if com.rank == 0:

            positionS = np.zeros((self.recvNode,self.dim))
            positionF = self.solver.getPosition()
            com.Recv(positionS,source=1)

            # Compute H and send its transpose to Solid

            self.computeMappingF(positionS,positionF)
            com.send(self.H.transpose(),dest=1)

        if com.rank == 1:
            
            self.H = None
            com.Send(self.solver.getPosition(),dest=0)
            self.H = com.recv(self.H,source=0)

# %% Mapping matrix from Solid to Fluid

    def phiTPS(self,dist):

        if dist > 0: return (dist*dist)*np.log10(dist)
        else: return 0



    def computeMappingF(self,positionS,positionF):

        A = np.zeros((self.nbrNode,self.recvNode+self.dim+1))
        B = np.zeros((self.recvNode+self.dim+1,self.recvNode+self.dim+1))
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

        A[:,0:self.recvNode] = Cfs
        A[:,self.recvNode:] = Pf

        B[:self.recvNode,:self.recvNode] = Css
        B[:self.recvNode,self.recvNode:] = Ps
        B[self.recvNode:,:self.recvNode] = Ps.T

        H = A.dot(np.linalg.inv(B))
        self.H = H[:,:self.recvNode]

        # Il vaut mieux calculer le LU de B une fois
        # pour ensuite résoudre avec un simple produit
        # Bx = b, B=LU, LUx=b, Ly=b, Ux=y

        # self.LUP = linalg.lu_factor(B)
        # Solution = linalg.lu_solve(self.LUP)


    # Interpolate recvData and return the result

    def interpData(self,recvData):
        return self.H.dot(recvData)
