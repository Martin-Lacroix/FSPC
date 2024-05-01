from .interpolator import Interpolator
from ..general import toolbox as tb
from functools import partial
import numpy as np

# Thin plate spline radial basis function

def thin_plate(position: np.ndarray, recv: np.ndarray, R: float):

    r = np.linalg.norm(position-recv, axis=1)
    return np.square(r/R)*np.ma.log(r/R)

# |-------------------------------------------|
# |   Thin Plate Spline Mesh Interpolation    |
# |-------------------------------------------|

class TPS(Interpolator):
    def __init__(self, radius: float):

        Interpolator.__init__(self)
        import multiprocessing as mp
        
        self.pool = mp.Pool(mp.cpu_count())
        self.radius = radius

    # Interpolate recv_data and return the result

    @tb.compute_time
    def interpolate(self, recv_data: np.ndarray):

        size = 1+tb.Solver.dim, np.size(recv_data, 1)
        result = np.append(recv_data, np.zeros(size), axis=0)
        result = np.linalg.lstsq(self.A, result, -1)[0]
        return np.dot(self.B, result)

# |-----------------------------------------------|
# |   Mapping Matrix from Recv_Pos to Position    |
# |-----------------------------------------------|

    @tb.compute_time
    def mapping(self, position: np.ndarray):

        size = 1+len(self.recv_pos)+tb.Solver.dim
        self.B = np.zeros((len(position), size))
        self.A = np.zeros((size, size))

        # Index ranges for an efficient vectorization

        K = range(len(position))
        N = range(len(self.recv_pos))
        L = range(1+len(self.recv_pos), size)

        # Initialize A without the basis function

        self.A[len(self.recv_pos), N] = 1
        self.A[N, len(self.recv_pos)] = 1
        self.A[np.ix_(N, L)] = self.recv_pos
        self.A[np.ix_(L, N)] = np.transpose(self.recv_pos)

        # Initialize B without the basis function

        self.B[np.ix_(K, L)] = position
        self.B[K, len(self.recv_pos)] = 1

        # Evaluate the radial basis function in parallel

        RBF = partial(thin_plate, recv=self.recv_pos, R=self.radius)

        self.B[np.ix_(K, N)] = self.pool.map(RBF, position)
        self.A[np.ix_(N, N)] = self.pool.map(RBF, self.recv_pos)
