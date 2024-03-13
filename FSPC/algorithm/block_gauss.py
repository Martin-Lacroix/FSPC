from mpi4py.MPI import COMM_WORLD as CW
from ..general import toolbox as tb
from .algorithm import Algorithm
import numpy as np

# |---------------------------------------------------|
# |   Block-Gauss Seidel Aitken Dynamic Relaxation    |
# |---------------------------------------------------|

class BGS(Algorithm):
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

        D = res_class.delta_res()
        A = np.tensordot(D, res_class.prev_res)

        # Update the Aitken relaxation parameter

        res_class.omega = -A*res_class.omega/np.tensordot(D, D)
        res_class.omega = max(min(res_class.omega, 1), 0)
        return res_class.omega*res_class.residual

# |-------------------------------------------------|
# |   Relaxation of Solid Interface Displacement    |
# |-------------------------------------------------|

    @tb.only_mechanical
    def update_displacement(self):

        if self.iteration > 0:
            tb.Interp.disp += self.compute(tb.ResMech)

        else:

            tb.ResMech.omega = self.omega
            tb.Interp.disp += self.omega*tb.ResMech.residual

# |------------------------------------------------|
# |   Relaxation of Solid Interface Temperature    |
# |------------------------------------------------|

    @tb.only_thermal
    def update_temperature(self):

        if self.iteration > 0:
            tb.Interp.temp += self.compute(tb.ResTher)

        else:
            
            tb.ResTher.omega = self.omega
            tb.Interp.temp += self.omega*tb.ResTher.residual
    