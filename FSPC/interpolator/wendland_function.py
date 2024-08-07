from .radial_basis_function import RBF
from functools import partial
import numpy as np

# Wendland C2 radial basis function interpolation class

class C2F(RBF):
    def __init__(self, radius: float):
        '''
        Initialize the wendland C2 interpolation class
        '''

        RBF.__init__(self)

        # Build a static basis_func(position, recv) with fixed radius

        basis_func = partial(self.wendland_function, R=radius)
        object.__setattr__(self, 'basis_func', basis_func)

    @staticmethod
    def wendland_function(position: np.ndarray, recv: np.ndarray, R: float):
        '''
        Return the value of the wendland function at the nodes
        '''

        # Compact support basis function where r/R is capped at one

        r = np.clip(np.linalg.norm(position-recv, axis=1)/R, 0, 1)
        return np.power(1-r, 4)*(4*r+1)
