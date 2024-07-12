from . import toolbox as tb
import numpy as np

# Coupling convergence and residual manager class

class Residual(tb.Static):
    def __init__(self, tol: float):
        '''
        Initialize the coupling convergence and residual manager class
        '''

        # User-defined tolerance and the residual to compare

        object.__setattr__(self, 'tol', tol)
        object.__setattr__(self, 'epsilon', np.inf)

        # Per-node version of the residual that is still dimensional

        object.__setattr__(self, 'prev_res', np.ndarray(0))
        object.__setattr__(self, 'residual', np.ndarray(0))

    def reset(self):
        '''
        Reset the class attributes to their default values
        '''

        self.prev_res = np.ndarray(0)
        self.residual = np.ndarray(0)

        # Initial epsilon should be higher than its first estimate

        self.epsilon = np.inf

    def update_res(self, result: np.ndarray, prediction: np.ndarray):
        '''
        Compute the residual and update the convergence criterion
        '''

        # Update the previous and current per-node residuals

        self.prev_res = np.copy(self.residual)
        self.residual = result-prediction

        # Compute the norm of the residual over each dimension

        res = np.linalg.norm(self.residual, axis=0)
        den = np.linalg.norm(result, axis=0)

        # Compute the norm of the dimensions then normalize

        res = res/(den+self.tol)
        self.epsilon = np.linalg.norm(res)

    def check(self):
        '''
        Returns true if the convergence criterion is satisfied
        '''

        # Return true if epsilon is smaller than the given tolerance

        if self.epsilon < self.tol: return True
        else: return False
    