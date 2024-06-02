from . import toolbox as tb
import numpy as np

# |---------------------------------------|
# |   Convergence and Residual Manager    |
# |---------------------------------------|

class Residual(tb.Frozen):
    def __init__(self, tol: float):

        self.__setattr__('tolerance', tol)
        self.__setattr__('epsilon', np.inf)

        # Current and previous residual vectors

        self.__setattr__('residual', np.ndarray(0))
        self.__setattr__('prev_res', np.ndarray(0))

        tb.Frozen.__init__(self)

    # Reset all the convergence indicators

    def reset(self):

        self.prev_res = np.ndarray(0)
        self.residual = np.ndarray(0)
        self.epsilon = np.inf

    # Update the current and previous residual

    def update_res(self, result: np.ndarray, prediction: np.ndarray):

        self.prev_res = np.copy(self.residual)
        self.residual = result-prediction

        res = np.linalg.norm(self.residual, axis=0)
        den = np.linalg.norm(result, axis=0)

        res = res/(den+self.tolerance)
        self.epsilon = np.linalg.norm(res)

    # Check if the convergence criterion is verified

    def check(self):

        if self.epsilon < self.tolerance: return True
        else: return False
    