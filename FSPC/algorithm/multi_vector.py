from ..general import toolbox as tb
from .block_gauss import BGS
import torch as pt

pt.set_grad_enabled(False)
pt.set_default_dtype(pt.double)

# Inverse least squares approximate Jacobian class

class InvJacobian(object):
    def __init__(self):
        '''
        Initialize the approximate inverse Jacobian class
        '''

        self.V = list()
        self.W = list()

        self.J = pt.zeros(0)
        self.prev_J = pt.zeros(0)

    def update(self):
        '''
        Copy the current Jacobian into the previous Jacobian
        '''

        self.prev_J = self.J.clone()

    def set_zero(self, size: int):
        '''
        Reset the class attributes to their default values
        '''

        self.J = pt.zeros((size, size))
        self.prev_J = pt.zeros((size, size))

    def delta(self, residual: pt.Tensor):
        '''
        Compute the predictor increment using the previous Jacobian
        '''

        V = pt.stack(self.V).transpose(0, 1).flip([1])
        W = pt.stack(self.W).transpose(0, 1).flip([1])
        R = pt.flatten(-residual)

        X = pt.transpose(W-self.prev_J.matmul(V), 0, 1)
        correction = pt.linalg.lstsq(V.transpose(0, 1), X, driver='gelsd').solution.transpose(0, 1)
        self.J = self.prev_J+correction

        delta = self.J.matmul(R)-R
        return delta.reshape(tb.Solver.get_size(), -1)

# Interface quasi-Newton with multi-vector Jacobian class

class MVJ(BGS):
    def __init__(self, max_iter: int):
        '''
        Initialize the interface quasi-Newton with multi-vector Jacobian class
        '''

        BGS.__init__(self, max_iter)

    @tb.only_solid
    def initialize(self):
        '''
        Reset the class attributes to their default values
        '''

        if tb.has_mecha: self.jac_mecha = InvJacobian()
        if tb.has_therm: self.jac_therm = InvJacobian()
    
    @tb.only_solid
    def update(self, verified: bool):
        '''
        Copy the current Jacobian into the previous Jacobian
        '''

        if not verified: return
        if tb.has_mecha: self.jac_mecha.update()
        if tb.has_therm: self.jac_therm.update()

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

            if not self.verified:

                self.jac_mecha.set_zero(tb.ResMech.residual.numel())
                delta = self.omega*tb.ResMech.residual

            else:

                R = pt.flatten(-tb.ResMech.residual)
                delta = self.jac_mecha.prev_J.matmul(R)-R
                delta = delta.reshape(tb.Solver.get_size(), -1)

        else:

            W = pt.flatten(disp-self.prev_disp)
            V = pt.flatten(tb.ResMech.residual-tb.ResMech.prev_res)

            self.jac_mecha.W.append(W)
            self.jac_mecha.V.append(V)

            delta = self.jac_mecha.delta(tb.ResMech.residual)

        # Update the pedicted displacement

        tb.Interp.disp += delta
        self.prev_disp = disp.clone()

    @tb.only_thermal
    def update_temperature(self):
        '''
        Update the predicted temperature with the predictor increment
        '''

        temp = tb.Solver.get_temperature()

        # Perform either BGS or IQN iteration

        if self.iteration == 0:

            self.jac_therm.V = list()
            self.jac_therm.W = list()

            if not self.verified:

                self.jac_therm.set_zero(tb.ResTher.residual.numel())
                delta = self.omega*tb.ResTher.residual

            else:

                R = pt.flatten(-tb.ResTher.residual)
                delta = self.jac_therm.prev_J.matmul(R)-R
                delta = delta.reshape(tb.Solver.get_size(), -1)

        else:

            W = pt.flatten(temp-self.prev_temp)
            V = pt.flatten(tb.ResTher.residual-tb.ResTher.prev_res)

            self.jac_therm.W.append(W)
            self.jac_therm.V.append(V)

            delta = self.jac_therm.delta(tb.ResTher.residual)

        # Update the pedicted temperature

        tb.Interp.temp += delta
        self.prev_temp = temp.clone()
