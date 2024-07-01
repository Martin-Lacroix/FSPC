import numpy as np

import torch as pt

pt.set_grad_enabled(False)
pt.set_default_dtype(pt.double)

# Coupling convergence and residual manager class

class Residual(object):
    def __init__(self, tol: float):
        '''
        Initialize the coupling convergence and residual manager class
        '''

        self.tol = tol
        self.reset()

    def reset(self):
        '''
        Reset the class attributes to their default values
        '''

        self.prev_res = pt.zeros(0)
        self.residual = pt.zeros(0)
        self.epsilon = np.inf

    def update_res(self, result: np.ndarray, prediction: np.ndarray):
        '''
        Compute the residual and update the convergence criterion
        '''

        self.prev_res = self.residual.clone()
        self.residual = result-prediction

        res = pt.norm(self.residual, dim=0)
        den = pt.norm(result, dim=0)

        res = res/(den+self.tol)
        self.epsilon = pt.norm(res)

    def check(self):
        '''
        Returns true if the convergence criterion is satisfied
        '''

        if self.epsilon < self.tol: return True
        else: return False
    