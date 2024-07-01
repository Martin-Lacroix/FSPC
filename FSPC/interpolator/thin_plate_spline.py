from .interpolator import Interpolator
from ..general import toolbox as tb
from functools import partial
import numpy as np

import torch as pt

pt.set_grad_enabled(False)
pt.set_default_dtype(pt.double)

# Thin plate spline radial basis function interpolation class

class TPS(Interpolator):
    def __init__(self, radius: float):
        '''
        Initialize the thin plate spline interpolation class
        '''

        Interpolator.__init__(self)
        self.radius = radius

        import multiprocessing as mp
        self.pool = mp.Pool(mp.cpu_count())

        import atexit
        atexit.register(self.pool.close)

    @tb.compute_time
    def interpolate(self, recv_data: np.ndarray):
        '''
        Return the interpolation from the source to the target mesh
        '''

        zeros = pt.zeros((1+tb.Solver.dim, recv_data.size(dim=1)))
        result = pt.vstack((recv_data, zeros))

        result = pt.linalg.lstsq(self.A, result).solution
        return pt.matmul(self.B, result).numpy()
    
    @staticmethod
    def basis_func(position: np.ndarray, recv: np.ndarray, R: float):
        '''
        Return the value of the thin plate spline at the nodes
        '''

        r = np.linalg.norm(position-recv, axis=1)/R
        return np.square(r)*np.ma.log(r)

    @tb.compute_time
    def mapping(self, position: np.ndarray):
        '''
        Compute the interpolation matrices from the source to the target
        '''

        size = 1+len(self.recv_pos)+tb.Solver.dim
        self.B = pt.zeros((len(position), size))
        self.A = pt.zeros((size, size))

        # Index ranges for an efficient vectorization

        K = range(len(position))
        N = range(len(self.recv_pos))
        L = range(1+len(self.recv_pos), size)

        # Initialize A without the basis function

        self.A[len(self.recv_pos), N] = 1
        self.A[N, len(self.recv_pos)] = 1
        self.A[np.ix_(N, L)] = self.recv_pos
        self.A[np.ix_(L, N)] = self.recv_pos.transpose(0, 1)

        # Initialize B without the basis function

        self.B[np.ix_(K, L)] = position
        self.B[K, len(self.recv_pos)] = 1

        # Evaluate the radial basis function in parallel

        RBF = partial(self.basis_func, recv=self.recv_pos.numpy(), R=self.radius)

        # self.B[np.ix_(K, N)] = self.pool.map(RBF, position)
        # self.A[np.ix_(N, N)] = self.pool.map(RBF, recv_pos)

        for i, line in enumerate(self.pool.map(RBF, position.numpy())): # Bad
            self.B[K[i], N] = pt.from_numpy(line)

        for i, line in enumerate(self.pool.map(RBF, self.recv_pos.numpy())): # Bad
            self.A[N[i], N] = pt.from_numpy(line)
