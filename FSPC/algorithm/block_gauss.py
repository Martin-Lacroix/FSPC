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

        # Omega is the user-defined initial Aitken relaxation

        object.__setattr__(self, 'omega', 0.5)
        object.__setattr__(self, 'iteration', 0)

        # Maximum number of iterations allowed for FSI coupling

        object.__setattr__(self, 'max_iter', max_iter)

        # Initialize the Aitken parameters with the provided one

        object.__setattr__(self, 'aitk_disp', self.omega)
        object.__setattr__(self, 'aitk_temp', self.omega)

    def coupling_algorithm(self):
        '''
        Run the fluid-structure coupling for the current time step
        '''

        self.iteration = 0

        # Loop until the maximum number of iterations is reached

        while self.iteration < self.max_iter:

            # Bring back the solvers to their last equilibrium state

            tb.Solver.way_back()

            # Break the while loop if the fluid solver failed

            self.transfer_dirichlet()
            if not tb.run_fluid(): break

            # Break the while loop if the solid solver failed

            self.transfer_neumann()
            if not tb.run_solid(): break

            # Update the predictor and check the coupling convergence

            verified = self.relaxation()

            # Share the convergence state to the fluid process

            verified = tb.com.bcast(verified, root=1)
            self.iteration += 1

            # Return true if the coupling algorithm has converged

            if verified: return True

        # Bring back the solvers to their last equilibrium state

        tb.Solver.way_back()
        return False

    @tb.only_mechanical
    def update_displacement(self):
        '''
        Compute the displacement predictor at the solid interface
        '''

        # We need a previous residual to update aitk_disp

        if self.iteration > 0:

            # Compute some temporary variables for Aitken relaxation

            D = tb.Res.residual_disp-tb.Res.prev_res_disp
            A = np.tensordot(D, tb.Res.prev_res_disp)

            # Update the mechanical Aitken relaxation parameter

            self.aitk_disp = -A*self.aitk_disp/np.tensordot(D, D)

            # Limit the Aitken parameter beteen zero and one

            self.aitk_disp = max(min(self.aitk_disp, 1), 0)

        # Use omega if no previous residual is available

        else: self.aitk_disp = self.omega

        # Update the predicted interface displacement

        tb.Interp.disp += self.aitk_disp*tb.Res.residual_disp

    @tb.only_thermal
    def update_temperature(self):
        '''
        Compute the temperature predictor at the solid interface
        '''

        # We need a previous residual to update aitk_temp

        if self.iteration > 0:

            # Compute some temporary variables for Aitken relaxation

            D = tb.Res.residual_temp-tb.Res.prev_res_temp
            A = np.tensordot(D, tb.Res.prev_res_temp)

            # Update the thermal Aitken relaxation parameter

            self.aitk_temp = -A*self.aitk_temp/np.tensordot(D, D)

            # Limit the Aitken parameter beteen zero and one

            self.aitk_temp = max(min(self.aitk_temp, 1), 0)

        # Use omega if no previous residual is available

        else: self.aitk_temp = self.omega

        # Update the predicted interface temperature

        tb.Interp.temp += self.aitk_temp*tb.Res.residual_temp
