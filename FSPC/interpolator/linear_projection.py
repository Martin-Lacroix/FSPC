from .interpolator import Interpolator
from scipy.sparse import dok_matrix
from ..general import toolbox as tb
import numpy as np

# Linear element projection interpolation class

class LEP(Interpolator):
    def __init__(self, elem_type: int):
        '''
        Initialize the linear element projection interpolation class
        '''

        Interpolator.__init__(self)

        match elem_type:

            case 2: self.element = Line()
            case 3: self.element = Triangle()

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

            # Find the closest neighbours in the reference mesh

            dist = np.linalg.norm(pos-self.recv_pos, axis=1)
            index = np.argsort(dist)[range(tb.Solver.dim)]
            recv_pos = self.recv_pos[index]

            # Project the point in the plane of the element

            param = self.element.projection(recv_pos, pos)
            self.H[i, index] = self.element.evaluate(param)

        self.H = self.H.tocsr()

# Linear 2D-line finite element class

class Line(object):

    def evaluate(self, parm: np.ndarray):
        '''
        Return the values of the shape functions in the parametric space
        '''

        return (1-parm[0])/2, (1+parm[0])/2

    def projection(self, node: np.ndarray, pos: np.ndarray):
        '''
        Return the projection of a global point in the parametric space
        '''

        A = np.diff(node, axis=0)/2
        B = np.array(pos-np.sum(node, axis=0)/2)
        return np.linalg.lstsq(np.transpose(A), B, -1)[0]

# Linear 3D-triangle finite element class

class Triangle(object):

    def evaluate(self, parm: np.ndarray):
        '''
        Return the values of the shape functions in the parametric space
        '''

        return 1-parm[0]-parm[1], parm[0], parm[1]

    def projection(self, node: np.ndarray, pos: np.ndarray):
        '''
        Return the projection of a global point in the parametric space
        '''

        B = np.array(pos-node[0])
        A = [node[1]-node[0], node[2]-node[0]]
        return np.linalg.lstsq(np.transpose(A), B, -1)[0]
