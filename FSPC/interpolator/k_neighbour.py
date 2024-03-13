from .interpolator import Interpolator
from scipy.sparse import dok_matrix
from ..general import toolbox as tb
import numpy as np

# |------------------------------------------------|
# |   Mesh Interpolation K - Nearest Neighbours    |
# |------------------------------------------------|

class KNN(Interpolator):
    def __init__(self, K: int):

        self.K = int(abs(K))

    # Compute the FS mesh interpolation matrix

    def initialize(self):

        Interpolator.__init__(self)
        position = tb.Solver.get_position()
        self.mapping(position)
        self.H = self.H.tocsr()

    # Interpolate recv_data and return the result

    @tb.compute_time
    def interpolate(self, recv_data: np.ndarray):
        return self.H.dot(recv_data)

# |----------------------------------------------|
# |   Mapping Matrix from RecvPos to Position    |
# |----------------------------------------------|

    @tb.compute_time
    def mapping(self, position: np.ndarray):

        self.H = dok_matrix(tb.Solver.get_size(), len(self.recv_pos))

        if self.K == 1: self.search(position)
        else: self.search_K(position)

# |------------------------------------|
# |   Find the K Nearest Neighbours    |
# |------------------------------------|

    def search(self, position: np.ndarray):

        for i, pos in enumerate(position):

            dist = np.linalg.norm(pos - self.recv_pos, axis=1)
            self.H[i, np.argmin(dist)] = 1

    def search_K(self, position: np.ndarray):

        for i, pos in enumerate(position):

            dist = np.linalg.norm(pos - self.recv_pos, axis=1)
            index = np.argsort(dist)[range(self.K)]
            weight = np.zeros(self.K)
            dist = dist[index]

            for j in range(self.K):

                val = [R for k, R in enumerate(dist) if k != j]
                weight[j] = np.prod(val)

            self.H[i, index] = weight/np.sum(weight)
