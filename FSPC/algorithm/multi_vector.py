from mpi4py.MPI import COMM_WORLD as CW
from ..general import toolbox as tb
from .algorithm import Algorithm
import numpy as np

# |---------------------------------------------------|
# |   Interface Quasi-Newton Multi-Vector Jacobian    |
# |---------------------------------------------------|

class MVJ(Algorithm):
    def __init__(self, max_iter: int):

        Algorithm.__init__(self)
        self.max_iter = max_iter
        self.omega = 0.5
        self.BGS = True

# |--------------------------------------|
# |   Coupling Algorithm at Each Step    |
# |--------------------------------------|

    def coupling_algorithm(self):

        self.iteration = 0
        while self.iteration < self.max_iter:

            # Transfer and fluid solver call

            self.transfer_dirichlet()
            if not self.run_fluid(): return False

            # Transfer and solid solver call

            self.transfer_neumann()
            if not self.run_solid(): return False

            # Compute the coupling residual

            output = self.relaxation()
            verified = CW.bcast(output, root=1)
            self.BGS = False

            # Exit the loop if the solution is converged

            self.iteration += 1
            if verified: self.update_prevJ(); return True
            self.way_back()

        self.BGS = True
        return False

# |--------------------------------------|
# |   Compute the Solution Correction    |
# |--------------------------------------|

    def compute(self, res_class: object):

        V = np.flip(np.transpose(res_class.V), axis=1)
        W = np.flip(np.transpose(res_class.W), axis=1)
        R = np.hstack(-res_class.residual)

        # Update the inverse Jacobian

        X = np.transpose(W-np.dot(res_class.prev_J, V))
        delta_J = np.transpose(np.linalg.lstsq(V.T, X, -1)[0])
        res_class.J = res_class.prev_J+delta_J

        # Return the solution correction

        delta = np.dot(res_class.J, R)-R
        return np.split(delta, tb.Solver.get_size())

# |-----------------------------------------------|
# |   Reset Jacobian and Perform BGS Iteration    |
# |-----------------------------------------------|

    def reset(self, res_class: object):

        size = res_class.residual.size
        res_class.J = np.zeros((size, size))
        res_class.prev_J = np.zeros((size, size))
        return self.omega*res_class.residual

    # Update the previous inverse Jacobian

    @tb.only_solid
    def update_prevJ(self):

        if tb.ResMech:
            tb.ResMech.prev_J = np.copy(tb.ResMech.J)

        if tb.ResTher:
            tb.ResTher.prev_J = np.copy(tb.ResTher.J)

# |-------------------------------------------------|
# |   Relaxation of Solid Interface Displacement    |
# |-------------------------------------------------|

    @tb.only_mechanical
    def update_displacement(self):

        disp = tb.Solver.get_position()

        # Perform either BGS or IQN iteration

        if self.iteration == 0:

            tb.ResMech.V = list()
            tb.ResMech.W = list()
            if self.BGS: delta = self.reset(tb.ResMech)

            else:

                R = np.hstack(-tb.ResMech.residual)
                delta = np.dot(tb.ResMech.prev_J, R)-R
                delta = np.split(delta, tb.Solver.get_size())

        else:

            tb.ResMech.V.append(np.hstack(tb.ResMech.delta_res()))
            tb.ResMech.W.append(np.hstack(disp-self.prev_disp))
            delta = self.compute(tb.ResMech)

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

            tb.ResTher.V = list()
            tb.ResTher.W = list()
            if self.BGS: delta = self.reset(tb.ResTher)
            else:

                R = np.hstack(-tb.ResTher.residual)
                delta = np.dot(tb.ResTher.prev_J, R)-R
                delta = np.split(delta, tb.Solver.get_size())

        else:

            tb.ResTher.V.append(np.hstack(tb.ResTher.delta_res()))
            tb.ResTher.W.append(np.hstack(temp-self.prev_temp))
            delta = self.compute(tb.ResTher)

        # Update the pedicted temperature

        tb.Interp.temp += delta
        self.prev_temp = np.copy(temp)
