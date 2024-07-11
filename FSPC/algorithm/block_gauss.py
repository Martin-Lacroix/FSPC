from ..general import toolbox as tb
from .algorithm import Algorithm
import numpy as np

# Block-Gauss Seidel Aitken dynamic relaxation class

class BGS(Algorithm):
    def __init__(self, max_iter: int):
        '''
        Initialize block-Gauss Seidel Aitken dynamic relaxation class
        '''

        Algorithm.__init__(self)

        object.__setattr__(self, 'omega', 0.5)
        object.__setattr__(self, 'iteration', 0)
        object.__setattr__(self, 'max_iter', max_iter)

        object.__setattr__(self, 'aitk_mecha', self.omega)
        object.__setattr__(self, 'aitk_mecha', self.omega)

    def coupling_algorithm(self):
        '''
        Run the fluid-structure coupling for the current time step
        '''

        self.iteration = 0

        while self.iteration < self.max_iter:

            tb.Solver.way_back()

            # Dirichlet transfer and fluid solver run

            self.transfer_dirichlet()
            if not tb.run_fluid(): break

            # Neumann transfer and solid solver run

            self.transfer_neumann()
            if not tb.run_solid(): break

            # Compute the coupling residual

            verified = self.relaxation()
            verified = tb.CW.bcast(verified, root=1)
            self.iteration += 1

            # Return true if the solution is converged

            if hasattr(self, 'update'): self.update(verified)
            if verified: return True

        tb.Solver.way_back()
        return False

    @tb.only_mechanical
    def update_displacement(self):
        '''
        Compute the displacement predictor at the solid interface
        '''

        if self.iteration > 0:

            D = tb.ResMech.residual-tb.ResMech.prev_res
            A = np.tensordot(D, tb.ResMech.prev_res)

            # Update the Aitken relaxation parameter

            self.aitk_mecha = -A*self.aitk_mecha/np.tensordot(D, D)
            self.aitk_mecha = max(min(self.aitk_mecha, 1), 0)

        else: self.aitk_mecha = self.omega
        tb.Interp.disp += self.aitk_mecha*tb.ResMech.residual

    @tb.only_thermal
    def update_temperature(self):
        '''
        Compute the temperature predictor at the solid interface
        '''

        if self.iteration > 0:

            D = tb.ResTher.residual-tb.ResTher.prev_res
            A = np.tensordot(D, tb.ResTher.prev_res)

            # Update the Aitken relaxation parameter

            self.aitk_therm = -A*self.aitk_therm/np.tensordot(D, D)
            self.aitk_therm = max(min(self.aitk_therm, 1), 0)

        else: self.aitk_therm = self.omega
        tb.Interp.temp += self.aitk_therm*tb.ResTher.residual
