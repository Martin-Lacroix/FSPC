from .interpolator import Interpolator
from ..general import toolbox as tb
import numpy as np

# Nearest neighbour interpolation class

class NNI(Interpolator):
    def __init__(self):
        '''
        Initialize the nearest neighbour interpolation class
        '''

        Interpolator.__init__(self)

        # Initialize the mesh interpolation sparse matrix

        object.__setattr__(self, 'H', np.ndarray(0))

    @tb.compute_time
    def interpolate(self, recv_data: np.ndarray):
        '''
        Return the interpolation from the source to the target mesh
        '''

        # We must use the dot method of the CSR matrix object

        return self.H.dot(recv_data)

    @tb.compute_time
    def mapping(self, position: np.ndarray):
        '''
        Compute the interpolation matrices from the source to the target
        '''

        # The dictionary of keys based matrix is suited for filling

        from scipy.sparse import dok_matrix
        self.H = dok_matrix((len(position), len(self.recv_pos)))

        # Loop on the positions of the nodes in the target mesh

        for i, pos in enumerate(position):

            # Find the closest neighbour node in the reference mesh

            dist = np.linalg.norm(pos-self.recv_pos, axis=1)
            self.H[i,np.argmin(dist)] = 1

        # Convert the dok matrix to compressed sparse row format

        self.H = self.H.tocsr()
