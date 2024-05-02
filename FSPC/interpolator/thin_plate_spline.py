from .interpolator import Interpolator
from ..general import toolbox as tb
from functools import partial

# Linear algebra parallelization library

import multiprocessing as mp
import scipy.linalg
import numpy as np

# Thin plate spline radial basis function

def basis_func(position: np.ndarray, recv: np.ndarray, R: float):

    r = np.linalg.norm(position-recv, axis=1)/R
    return np.square(r)*np.ma.log(r)

# |-------------------------------------------|
# |   Thin Plate Spline Mesh Interpolation    |
# |-------------------------------------------|

class TPS(Interpolator):
    def __init__(self, radius: float):

        Interpolator.__init__(self)
    
        
        self.pool = mp.Pool(mp.cpu_count())
        self.radius = radius

    # Interpolate recv_data and return the result

    @tb.compute_time
    def interpolate(self, recv_data: np.ndarray):

        zeros = np.zeros((1+tb.Solver.dim, np.size(recv_data, 1)))
        result = np.vstack((recv_data, zeros))

        result = scipy.linalg.solve(self.A, result, assume_a='sym')
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

        RBF = partial(basis_func, recv=self.recv_pos, R=self.radius)

        self.B[np.ix_(K, N)] = self.pool.map(RBF, position)
        self.A[np.ix_(N, N)] = self.pool.map(RBF, self.recv_pos)
