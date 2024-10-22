from .radial_basis_function import RBF
import numpy as np

# Thin plate spline radial basis function interpolation class

class TPS(RBF):
    def __init__(self, radius: float):
        '''
        Initialize the thin plate spline interpolation class
        '''

        RBF.__init__(self)
        from functools import partial

        # Build a static basis_func(position, recv) with fixed radius

        basis_func = partial(self.thin_plate_spline, R=radius)
        object.__setattr__(self, 'basis_func', basis_func)

    @staticmethod
    def thin_plate_spline(position: np.ndarray, recv: np.ndarray, R: float):
        '''
        Return the value of the thin plate spline at the nodes
        '''

        # Use broadcasting to compute the pairwise distances

        difference = position[:, np.newaxis, :]-recv[np.newaxis, :, :]
        r = np.linalg.norm(difference, axis=2)/R

        # Global support basis function where ma.log(zero) = zero

        return np.square(r)*np.ma.log(r)
