from ..general import toolbox as tb
from .block_gauss import BGS
import numpy as np

# |--------------------------------------------|
# |   Class of Approximate Inverse Jacobian    |
# |--------------------------------------------|

class InvJacobian(object):
    def __init__(self):

        self.V = list()
        self.W = list()

        self.J = np.ndarray(0)
        self.prev_J = np.ndarray(0)

    def update(self):

        self.prev_J = np.copy(self.J)

    def set_zero(self, size):

        self.J = np.zeros((size, size))
        self.prev_J = np.zeros((size, size))

    # Compute the solution correction

    def delta(self, residual: np.ndarray):

        V = np.flip(np.transpose(self.V), axis=1)
        W = np.flip(np.transpose(self.W), axis=1)
        R = np.hstack(-residual)

        # Update the inverse Jacobian

        X = np.transpose(W-np.dot(self.prev_J, V))
        correction = np.transpose(np.linalg.lstsq(V.T, X, -1)[0])
        self.J = self.prev_J+correction

        # Return the solution correction

        delta = np.dot(self.J, R)-R
        return np.split(delta, tb.Solver.get_size())

# |---------------------------------------------------|
# |   Interface Quasi-Newton Multi-Vector Jacobian    |
# |---------------------------------------------------|

class MVJ(BGS):
    def __init__(self, max_iter: int):
        BGS.__init__(self, max_iter)

    @tb.only_solid
    def initialize(self):

        if tb.has_mecha: self.jac_mecha = InvJacobian()
        if tb.has_therm: self.jac_therm = InvJacobian()
    
    @tb.only_solid
    def update(self, verified):

        if not verified: return
        if tb.has_mecha: self.jac_mecha.update()
        if tb.has_therm: self.jac_therm.update()

# |-------------------------------------------------|
# |   Relaxation of Solid Interface Displacement    |
# |-------------------------------------------------|

    @tb.only_mechanical
    def update_displacement(self):

        disp = tb.Solver.get_position()

        # Perform either BGS or IQN iteration

        if self.iteration == 0:

            self.jac_mecha.V = list()
            self.jac_mecha.W = list()

            if not self.verified:

                self.jac_mecha.set_zero(tb.ResMech.residual.size)
                delta = self.omega*tb.ResMech.residual

            else:

                R = np.hstack(-tb.ResMech.residual)
                delta = np.dot(self.jac_mecha.prev_J, R)-R
                delta = np.split(delta, tb.Solver.get_size())

        else:

            W = np.hstack(disp-self.prev_disp)
            V = np.hstack(tb.ResMech.residual-tb.ResMech.prev_res)

            self.jac_mecha.W.append(W)
            self.jac_mecha.V.append(V)

            delta = self.jac_mecha.delta(tb.ResMech.residual)

        # Update the pedicted displacement

        tb.Interp.disp += delta
        self.prev_disp = np.copy(disp)

# |------------------------------------------------|
# |   Relaxation of Solid Interface Temperature    |
# |------------------------------------------------|

    @tb.only_thermal
    def update_temperature(self):

        temp = tb.Solver.get_temperature()

        # Perform either BGS or IQN iteration

        if self.iteration == 0:

            self.jac_therm.V = list()
            self.jac_therm.W = list()

            if not self.verified:

                self.jac_therm.set_zero(tb.ResTher.residual.size)
                delta = self.omega*tb.ResTher.residual

            else:

                R = np.hstack(-tb.ResTher.residual)
                delta = np.dot(self.jac_therm.prev_J, R)-R
                delta = np.split(delta, tb.Solver.get_size())

        else:

            W = np.hstack(temp-self.prev_temp)
            V = np.hstack(tb.ResTher.residual-tb.ResTher.prev_res)

            self.jac_therm.W.append(W)
            self.jac_therm.V.append(V)

            delta = self.jac_therm.delta(tb.ResTher.residual)

        # Update the pedicted temperature

        tb.Interp.temp += delta
        self.prev_temp = np.copy(temp)
