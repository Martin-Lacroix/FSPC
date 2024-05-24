from .interpolator import Interpolator
from scipy.sparse import dok_matrix
from ..general import toolbox as tb
import numpy as np

# |--------------------------------------|
# |   Nearest Neighbour Interpolation    |
# |--------------------------------------|

class NNI(Interpolator):
    def __init__(self):

        Interpolator.__init__(self)

    # Interpolate recv_data and return the result

    @tb.compute_time
    def interpolate(self, recv_data: np.ndarray):
        return self.H.dot(recv_data)

# |----------------------------------------------|
# |   Mapping Matrix from RecvPos to Position    |
# |----------------------------------------------|

    @tb.compute_time
    def mapping(self, position: np.ndarray):

        self.H = dok_matrix((len(position), len(self.recv_pos)))

        for i, pos in enumerate(position):

            # Find the closest neighbour in the reference mesh

            dist = np.linalg.norm(pos-self.recv_pos, axis=1)
            self.H[i,np.argmin(dist)] = 1

        self.H = self.H.tocsr()
