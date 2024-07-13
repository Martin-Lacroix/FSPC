from .interpolator import Interpolator
from ..general import toolbox as tb
from scipy import linalg
import numpy as np

# Base radial basis function interpolation class

class RBF(Interpolator):
    def __init__(self):
        '''
        Initialize the thin plate spline interpolation class
        '''

        Interpolator.__init__(self)

        # Multiprocessing pool for nodal distance computation

        import multiprocessing as mp
        object.__setattr__(self, 'pool', mp.Pool(mp.cpu_count()))

        # Close the multiprocessing pool before class destructor

        import atexit
        atexit.register(self.pool.close)

        # Initialize the mesh interpolation matrices

        object.__setattr__(self, 'A', np.ndarray(0))
        object.__setattr__(self, 'B', np.ndarray(0))

    @tb.compute_time
    def interpolate(self, recv_data: np.ndarray):
        '''
        Return the interpolation from the source to the target mesh
        '''

        # Add dim + 1 lines of zeros to the source vector

        zeros = np.zeros((1+tb.Solver.dim, np.size(recv_data, 1)))
        result = np.vstack((recv_data, zeros))

        # The QR-based Lapack solver is suitable for singular matrices

        result = linalg.lapack.dgels(self.A, result)[1]
        return np.dot(self.B, result)

    @tb.compute_time
    def mapping(self, position: np.ndarray):
        '''
        Compute the interpolation matrices from the source to the target
        '''

        size = 1+len(self.recv_pos)+tb.Solver.dim

        # Initialize the mesh interpolation matrices to zero

        self.B = np.zeros((len(position), size))
        self.A = np.zeros((size, size))

        # Build index ranges for an efficient array vectorization

        K = range(len(position))
        N = range(len(self.recv_pos))
        L = range(1+len(self.recv_pos), size)

        # Add the constant polynomial term to the A matrix

        self.A[len(self.recv_pos), N] = 1
        self.A[N, len(self.recv_pos)] = 1

        # Add the x, y and z polynomial terms to the A matrix

        self.A[np.ix_(N, L)] = self.recv_pos
        self.A[np.ix_(L, N)] = np.transpose(self.recv_pos)

        # Add the polynomial terms to the right of the B matrix

        self.B[np.ix_(K, L)] = position
        self.B[K, len(self.recv_pos)] = 1

        # Build a static basis_func(position) with a single parameter

        from functools import partial
        func = partial(self.basis_func, recv=self.recv_pos)

        # Evaluate the radial basis function in parallel

        self.B[np.ix_(K, N)] = self.pool.map(func, position)
        self.A[np.ix_(N, N)] = self.pool.map(func, self.recv_pos)
