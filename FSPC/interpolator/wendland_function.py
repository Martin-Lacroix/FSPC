from .radial_basis_function import RBF
import numpy as np

# Wendland C2 radial basis function interpolation class

class C2F(RBF):
    def __init__(self, radius: float):
        '''
        Initialize the wendland C2 interpolation class
        '''

        RBF.__init__(self)
        from functools import partial

        # Build a static basis_func(position, recv) with fixed radius

        basis_func = partial(self.wendland_function, R=radius)
        object.__setattr__(self, 'basis_func', basis_func)

    @staticmethod
    def wendland_function(position: np.ndarray, recv: np.ndarray, R: float):
        '''
        Return the value of the wendland function at the nodes
        '''

        # Use broadcasting to compute the pairwise distances

        difference = position[:, np.newaxis, :]-recv[np.newaxis, :, :]
        r = np.clip(np.linalg.norm(difference, axis=2)/R, 0, 1)

        # Compact support basis function where r/R is capped at one

        return np.power(1-r, 4)*(4*r+1)
