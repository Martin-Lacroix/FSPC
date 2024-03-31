from .interpolator import Interpolator
from scipy.sparse import dok_matrix
from ..general import toolbox as tb
import numpy as np

# |----------------------------------------------|
# |   Mesh Interpolation K-Nearest Neighbours    |
# |----------------------------------------------|

class LEP(Interpolator):
    def __init__(self):

        Interpolator.__init__(self)
        if tb.Solver.dim == 2: self.element = Line()
        if tb.Solver.dim == 3: self.element = Triangle()

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

            # Find the closest neighbours in the reference mesh

            dist = np.linalg.norm(pos-self.recv_pos, axis=1)
            index = np.argsort(dist)[range(tb.Solver.dim)]
            recv_pos = self.recv_pos[index]

            # Project the point in the plane of the element

            param = self.element.projection(recv_pos, pos)
            self.H[i, index] = self.element.evaluate(param)

        self.H = self.H.tocsr()

# |---------------------------------------|
# |   Linear 2D and 3D Finite Elements    |
# |---------------------------------------|

class Line(object):

    def evaluate(self, parm: np.ndarray):

        return (1-parm[0])/2, (1+parm[0])/2
    
    # Projection of a point in the parametric space

    def projection(self, node: np.ndarray, pos: np.ndarray):

        A = np.diff(node, axis=0)/2
        B = np.array(pos-np.sum(node, axis=0)/2)
        return np.linalg.lstsq(np.transpose(A), B, -1)[0]

class Triangle(object):

    def evaluate(self, parm: np.ndarray):

        return 1-parm[0]-parm[1], parm[0], parm[1]

    # Projection of a point in the parametric space

    def projection(self, node: np.ndarray, pos: np.ndarray):

        B = np.array(pos-node[0])
        A = [node[1]-node[0], node[2]-node[0]]
        return np.linalg.lstsq(np.transpose(A), B, -1)[0]
