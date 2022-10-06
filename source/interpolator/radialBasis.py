from .interpolator import Interpolator
import numpy as np

# %% Energy Conservative Radial Basis Function

class NM_RBF(Interpolator):
    def __init__(self,input,param,com):
        Interpolator.__init__(self,input,com)

        # Defines the radial basis function

        self.radius = param['radius']
        self.function = getattr(self,'phi'+param['RBF'])
        recvPos = np.zeros((self.recvNode,self.dim))

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

        # Compute the interpolation  H matrix

        self.H = np.linalg.solve(A.T,B.T).T
        self.H = self.H[:self.nbrNode,:self.recvNode]

# %% Interpolate recvData and return the result

    def interpDataSF(self,recvData):

        # count = 0
        # recvData = np.zeros(recvData.shape)
        # for i in range(recvData.shape[0]):
        #     recvData[i,0] += count
        #     count += 1


        # f = open("TEST.txt", "a")
        # f.write('\n\n[uS] Matrix\n')

        # for i in range(recvData.shape[0]):
        #     for j in range(recvData.shape[1]):
        #         f.write('{:.4e}'.format(recvData[i,j]).ljust(15))

        #     f.write('\n')
        # f.close()

        # recvData2 = self.H.dot(recvData)

        # f = open("TEST.txt", "a")
        # f.write('\n\n[uF] Matrix\n')

        # for i in range(recvData2.shape[0]):
        #     for j in range(recvData2.shape[1]):
        #         f.write('{:.4e}'.format(recvData2[i,j]).ljust(15))

        #     f.write('\n')
        # f.close()

        # raise Exception('END')

        return self.H.dot(recvData)

    def interpDataFS(self,recvData):

        # f = open("TEST.txt", "a")
        # f.write('\n\n[fF] Matrix\n')

        # for i in range(recvData.shape[0]):
        #     for j in range(recvData.shape[1]):
        #         f.write('{:.4e}'.format(recvData[i,j]).ljust(15))

        #     f.write('\n')
        # f.close()
        

        # recvData2 = self.H.dot(recvData)

        # f = open("TEST.txt", "a")
        # f.write('\n\n[fS] Matrix\n')

        # for i in range(recvData2.shape[0]):
        #     for j in range(recvData2.shape[1]):
        #         f.write('{:.4e}'.format(recvData2[i,j]).ljust(15))

        #     f.write('\n')
        # f.close()

        # raise Exception('END')

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
