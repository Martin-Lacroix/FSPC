from .radial_basis_function import RBF
from functools import partial
import numpy as np

# Thin plate spline radial basis function interpolation class

class TPS(RBF):
    def __init__(self, radius: float):
        '''
        Initialize the thin plate spline interpolation class
        '''

        RBF.__init__(self)

        # Build a static basis_func(position, recv) with fixed radius

        basis_func = partial(self.thin_plate_spline, R=radius)
        object.__setattr__(self, 'basis_func', basis_func)
    
    @staticmethod
    def thin_plate_spline(position: np.ndarray, recv: np.ndarray, R: float):
        '''
        Return the value of the thin plate spline at the nodes
        '''

        # Global support basis function where ma.log(zero) = zero

        r = np.linalg.norm(position-recv, axis=1)/R
        return np.square(r)*np.ma.log(r)
