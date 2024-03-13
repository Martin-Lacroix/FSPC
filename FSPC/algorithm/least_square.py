from mpi4py.MPI import COMM_WORLD as CW
from ..general import toolbox as tb
from .algorithm import Algorithm
import numpy as np

# |--------------------------------------------------|
# |   Interface Quasi-Newton Inverse Least Square    |
# |--------------------------------------------------|

class ILS(Algorithm):
    def __init__(self, max_iter: int):

        Algorithm.__init__(self)
        self.max_iter = max_iter
        self.omega = 0.5

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

            # Exit the loop if the solution is converged

            self.iteration += 1
            if verified: return True
            else: self.way_back()

        return False

# |--------------------------------------|
# |   Compute the Solution Correction    |
# |--------------------------------------|

    def compute(self, res_class: object):

        V = np.flip(np.transpose(res_class.V), axis=1)
        W = np.flip(np.transpose(res_class.W), axis=1)
        R = np.hstack(-res_class.residual)

        # Return the solution correction

        delta = np.dot(W, np.linalg.lstsq(V, R, -1)[0]) - R
        return np.split(delta, tb.Solver.get_size())

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
            delta = self.omega*tb.ResMech.residual

        else:

            tb.ResMech.V.append(np.hstack(tb.ResMech.delta_res()))
            tb.ResMech.W.append(np.hstack(disp - self.prev_disp))
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
            delta = self.omega*tb.ResTher.residual

        else:
            
            tb.ResTher.V.append(np.hstack(tb.ResTher.delta_res()))
            tb.ResTher.W.append(np.hstack(temp - self.prev_temp))
            delta = self.compute(tb.ResTher)

        # Update the predicted temperature

        tb.Interp.temp += delta
        self.prev_temp = np.copy(temp)
