from .Interpolator import Interpolator
from ..general import Toolbox as tb
import numpy as np

# |------------------------------------------------|
# |   Mesh Interpolation Radial Basis Functions    |
# |------------------------------------------------|

class RBF(Interpolator):
    def __init__(self,func):
        self.function = func

    # Compute the FS mesh interpolation matrix

    def initialize(self):

        Interpolator.__init__(self)
        position = tb.Solver.getPosition()
        self.__mapping(position)

    # Interpolate recvData and return the result

    @tb.compute_time
    def interpData(self,recvData):

        size = (tb.Solver.dim+1,np.size(recvData,1))
        result = np.append(recvData,np.zeros(size),axis=0)
        result = np.linalg.lstsq(self.A,result,-1)[0]
        return np.dot(self.B,result)

# |----------------------------------------------|
# |   Mapping Matrix from RecvPos to Position    |
# |----------------------------------------------|

    @tb.compute_time
    def __mapping(self,position):

        self.size = 1+tb.Solver.dim+len(self.recvPos)
        self.B = self.__makeB(position)
        self.A = self.__makeA()

        # Fill A and B with radial basis function

        K = range(len(position))
        N = range(len(self.recvPos))

        for i,pos in enumerate(self.recvPos):

            rad = np.linalg.norm(pos-position,axis=1)
            self.B[K,i] = self.function(rad)

            rad = np.linalg.norm(pos-self.recvPos,axis=1)
            self.A[i,N] = self.function(rad)

# |--------------------------------------|
# |   Initialize the A and B Matrices    |
# |--------------------------------------|

    def __makeA(self):

        N = len(self.recvPos)
        K = range(1+N,self.size)
        A = np.zeros((self.size,self.size))

        # Initialize A with target mesh positions

        A[N,range(N)] = A[range(N),N] = 1
        A[np.ix_(range(N),K)] = self.recvPos
        A[np.ix_(K,range(N))] = np.transpose(self.recvPos)
        return A

    # Initialize B with reference mesh positions

    def __makeB(self,position):

        N = len(position)
        B = np.ones((N,self.size))
        K = range(1+len(self.recvPos),self.size)
        B[np.ix_(range(N),K)] = position
        return B
