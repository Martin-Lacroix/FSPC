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

    # Compute the solution correction

    def delta(self, residual: np.ndarray):

        V = np.flip(np.transpose(self.V), axis=1)
        W = np.flip(np.transpose(self.W), axis=1)
        R = np.hstack(-residual)

        # Return the solution correction

        delta = np.dot(W, np.linalg.lstsq(V, R, -1)[0])-R
        return np.split(delta, tb.Solver.get_size())

# |--------------------------------------------------|
# |   Interface Quasi-Newton Inverse Least Square    |
# |--------------------------------------------------|

class ILS(BGS):
    def __init__(self, max_iter: int):
        BGS.__init__(self, max_iter)

    @tb.only_solid
    def initialize(self):

        if tb.has_mecha: self.jac_mecha = InvJacobian()
        if tb.has_therm: self.jac_therm = InvJacobian()

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

# |------------------------------------------------|
# |   Relaxation of Solid Interface Temperature    |
# |------------------------------------------------|

    @tb.only_thermal
    def update_temperature(self):

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
