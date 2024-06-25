from ..general import toolbox as tb
from .block_gauss import BGS
import numpy as np

# Inverse least squares approximate Jacobian class

class InvJacobian(object):
    def __init__(self):
        '''
        Initialize the approximate inverse Jacobian class
        '''

        self.V = list()
        self.W = list()

    def delta(self, residual: np.ndarray):
        '''
        Compute the predictor increment using the current Jacobian
        '''

        V = np.flip(np.transpose(self.V), axis=1)
        W = np.flip(np.transpose(self.W), axis=1)
        R = np.hstack(-residual)

        # Return the solution correction increment

        delta = np.dot(W, np.linalg.lstsq(V, R, -1)[0])-R
        return np.split(delta, tb.Solver.get_size())

# Interface quasi-Newton with inverse least squares class

class ILS(BGS):
    def __init__(self, max_iter: int):
        '''
        Initialize the interface quasi-Newton with inverse least squares class
        '''

        BGS.__init__(self, max_iter)

    @tb.only_solid
    def initialize(self):
        '''
        Reset the class attributes to their default values
        '''

        if tb.has_mecha: self.jac_mecha = InvJacobian()
        if tb.has_therm: self.jac_therm = InvJacobian()

    @tb.only_mechanical
    def update_displacement(self):
        '''
        Update the predicted displacement with the predictor increment
        '''

        disp = tb.Solver.get_position()

        # Perform either BGS or IQN iteration

        if self.iteration == 0:

            self.jac_mecha.V = list()
            self.jac_mecha.W = list()
            delta = self.omega*tb.ResMech.residual

        else:

            W = np.hstack(disp-self.prev_disp)
            V = np.hstack(tb.ResMech.residual-tb.ResMech.prev_res)

            self.jac_mecha.W.append(W)
            self.jac_mecha.V.append(V)

            delta = self.jac_mecha.delta(tb.ResMech.residual)

        # Update the pedicted displacement

        tb.Interp.disp += delta
        self.prev_disp = np.copy(disp)

    @tb.only_thermal
    def update_temperature(self):
        '''
        Update the predicted temperature with the predictor increment
        '''

        temp = tb.Solver.get_temperature()

        # Perform either BGS or IQN iteration

        if self.iteration == 0:

            self.jac_mecha.V = list()
            self.jac_mecha.W = list()
            delta = self.omega*tb.ResTher.residual

        else:

            W = np.hstack(temp-self.prev_temp)
            V = np.hstack(tb.ResTher.residual-tb.ResTher.prev_res)

            self.jac_therm.W.append(W)
            self.jac_therm.V.append(V)

            delta = self.jac_therm.delta(tb.ResTher.residual)

        # Update the predicted temperature

        tb.Interp.temp += delta
        self.prev_temp = np.copy(temp)
