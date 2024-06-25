from .interpolator import Interpolator
from scipy.sparse import dok_matrix
from ..general import toolbox as tb
import numpy as np

# Nearest neighbour interpolation class

class NNI(Interpolator):
    def __init__(self):
        '''
        Initialize the nearest neighbour interpolation class
        '''

        Interpolator.__init__(self)

    @tb.compute_time
    def interpolate(self, recv_data: np.ndarray):
        '''
        Return the interpolation from the source to the target mesh
        '''

        return self.H.dot(recv_data)

    @tb.compute_time
    def mapping(self, position: np.ndarray):
        '''
        Compute the interpolation matrices from the source to the target
        '''

        self.H = dok_matrix((len(position), len(self.recv_pos)))

        for i, pos in enumerate(position):

            # Find the closest neighbour in the reference mesh

            dist = np.linalg.norm(pos-self.recv_pos, axis=1)
            self.H[i,np.argmin(dist)] = 1

        self.H = self.H.tocsr()
