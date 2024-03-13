from .interpolator import Interpolator
from ..general import toolbox as tb
import numpy as np

# |------------------------------------------------|
# |   Mesh Interpolation Radial Basis Functions    |
# |------------------------------------------------|

class RBF(Interpolator):
    def __init__(self, func: object):

        self.function = func

    # Compute the FS mesh interpolation matrix

    def initialize(self):

        Interpolator.__init__(self)
        position = tb.Solver.get_position()
        self.mapping(position)

    # Interpolate recv_data and return the result

    @tb.compute_time
    def interpolate(self, recv_data: np.ndarray):

        size = (tb.Solver.dim + 1, np.size(recv_data, 1))
        result = np.append(recv_data, np.zeros(size), axis=0)
        result = np.linalg.lstsq(self.A, result, -1)[0]
        return np.dot(self.B, result)

# |-----------------------------------------------|
# |   Mapping Matrix from Recv_Pos to Position    |
# |-----------------------------------------------|

    @tb.compute_time
    def mapping(self, position: np.ndarray):

        self.size = 1 + tb.Solver.dim + len(self.recv_pos)
        self.B = self.compute_B(position)
        self.A = self.compute_A()

        # Fill A and B with radial basis function

        K = range(len(position))
        N = range(len(self.recv_pos))

        for i, pos in enumerate(self.recv_pos):

            rad = np.linalg.norm(pos - position, axis=1)
            self.B[K, i] = self.function(rad)

            rad = np.linalg.norm(pos - self.recv_pos, axis=1)
            self.A[i, N] = self.function(rad)

# |--------------------------------------|
# |   Initialize the A and B Matrices    |
# |--------------------------------------|

    def compute_A(self):

        N = len(self.recv_pos)
        K = range(1 + N, self.size)
        A = np.zeros((self.size, self.size))

        # Initialize A with target mesh positions

        A[N, range(N)] = A[range(N), N] = 1
        A[np.ix_(range(N), K)] = self.recv_pos
        A[np.ix_(K, range(N))] = np.transpose(self.recv_pos)
        return A

    # Initialize B with reference mesh positions

    def compute_B(self, position: np.ndarray):

        N = len(position)
        B = np.ones((N, self.size))
        K = range(1 + len(self.recv_pos), self.size)
        B[np.ix_(range(N), K)] = position
        return B
