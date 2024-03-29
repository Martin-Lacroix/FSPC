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

    @tb.only_solid
    def initialize(self):

        if tb.has_mecha: self.aitk_mecha = self.omega
        if tb.has_therm: self.aitk_therm = self.omega

# |--------------------------------------|
# |   Coupling Algorithm at Each Step    |
# |--------------------------------------|

    def coupling_algorithm(self):
        
        verified = False
        self.iteration = 0

        while self.iteration < self.max_iter:

            # Dirichlet transfer and fluid solver run

            self.transfer_dirichlet()

            if CW.rank == 0:

                verified = tb.Solver.run()
                if not verified: tb.Solver.way_back()

            verified = CW.bcast(verified, root=0)
            if not verified: return False

            # Neumann transfer and solid solver run

            self.transfer_neumann()

            if CW.rank == 1: verified = tb.Solver.run()
            verified = CW.bcast(verified, root=1)

            if not verified:
                
                tb.Solver.way_back()
                return False

            # Compute the coupling residual

            verified = self.relaxation()
            verified = CW.bcast(verified, root=1)
            self.iteration += 1

            # Return true if the solution is converged

            if hasattr(self, 'update'): self.update(verified)
            if verified: return True
            tb.Solver.way_back()

        return False

# |-------------------------------------------------|
# |   Relaxation of Solid Interface Displacement    |
# |-------------------------------------------------|

    @tb.only_mechanical
    def update_displacement(self):

        if self.iteration > 0:

            D = tb.ResMech.residual-tb.ResMech.prev_res
            A = np.tensordot(D, tb.ResMech.prev_res)

            # Update the Aitken relaxation parameter

            self.aitk_mecha = -A*self.aitk_mecha/np.tensordot(D, D)
            self.aitk_mecha = max(min(self.aitk_mecha, 1), 0)

        else: self.aitk_mecha = self.omega
        tb.Interp.disp += self.aitk_mecha*tb.ResMech.residual

# |------------------------------------------------|
# |   Relaxation of Solid Interface Temperature    |
# |------------------------------------------------|

    @tb.only_thermal
    def update_temperature(self):

        if self.iteration > 0:

            D = tb.ResTher.residual-tb.ResTher.prev_res
            A = np.tensordot(D, tb.ResTher.prev_res)

            # Update the Aitken relaxation parameter

            self.aitk_therm = -A*self.aitk_therm/np.tensordot(D, D)
            self.aitk_therm = max(min(self.aitk_therm, 1), 0)

        else: self.aitk_therm = self.omega
        tb.Interp.temp += self.aitk_therm*tb.ResTher.residual
