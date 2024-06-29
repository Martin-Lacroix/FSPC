from .interpolator import Interpolator
from ..general import toolbox as tb
from functools import partial
import numpy as np

# Check if Pytorch and CUDA are available

try:
    
    import torch as tr
    if not tr.cuda.is_available(): raise Exception('CUDA not found')

except: raise Exception('Pytorch package not found')

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

        size = 1+tb.Solver.dim, np.size(recv_data, 1)
        zeros = tr.zeros((size), device='cuda')

        result = tr.from_numpy(recv_data).to(device='cuda')
        result = tr.vstack((result, zeros))

        # Solve the linear system on GPU and send it to the CPU

        result = tr.linalg.lstsq(self.A, result).solution
        return tr.matmul(self.B, result).cpu().numpy()
    
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
        B = np.zeros((len(position), size))
        A = np.zeros((size, size))

        # Index ranges for an efficient vectorization

        K = range(len(position))
        N = range(len(self.recv_pos))
        L = range(1+len(self.recv_pos), size)

        # Initialize A without the basis function

        A[len(self.recv_pos), N] = 1
        A[N, len(self.recv_pos)] = 1
        A[np.ix_(N, L)] = self.recv_pos
        A[np.ix_(L, N)] = np.transpose(self.recv_pos)

        # Initialize B without the basis function

        B[np.ix_(K, L)] = position
        B[K, len(self.recv_pos)] = 1

        # Evaluate the radial basis function in parallel

        RBF = partial(self.basis_func, recv=self.recv_pos, R=self.radius)

        B[np.ix_(K, N)] = self.pool.map(RBF, position)
        A[np.ix_(N, N)] = self.pool.map(RBF, self.recv_pos)

        # Move the interpolation matrices to the GPU

        tr.cuda.empty_cache()

        self.A = tr.from_numpy(A).to(device='cuda')
        self.B = tr.from_numpy(B).to(device='cuda')
