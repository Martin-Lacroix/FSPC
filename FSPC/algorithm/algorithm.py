from ..general import toolbox as tb

# Base fluid-structure coupling algorithm class

class Algorithm(tb.Static):

    @tb.compute_time
    def simulate(self, end_time: float):
        '''
        Run the fluid-structure simulation algorithm
        '''
        
        object.__setattr__(self, 'verified', False)

        # Export the initial solver state on the disk

        tb.Solver.save()

        # Loop over the time steps of the FSI coupling

        while tb.Step.time < end_time:

            tb.Step.display_time_step()

            # Build the interpolation matrices and reset the residual 

            tb.Interp.initialize()
            tb.Res.reset()

            # Initial guess for the equilibrium interface solution

            self.compute_predictor()

            # Perform the coupling iterations and update the time step

            self.verified = self.coupling_algorithm()
            tb.Step.update_time()

            # Fluid remeshing and update the solution exporter

            if self.verified:

                tb.Solver.update()
                tb.Step.update_exporter()

    @tb.only_solid
    def compute_predictor(self):
        '''
        Predict the future solution at the solid interface
        '''

        # The functions run only if their respective coupling is enabled

        tb.Interp.predict_temperature()
        tb.Interp.predict_displacement()

    @tb.only_solid
    @tb.compute_time
    def relaxation(self):
        '''
        Compute the predicted solution at the solid interface
        '''

        # Compute the residual between the predictor and Metafor

        tb.Res.update_res_mech()
        tb.Res.update_res_ther()

        # Update the predictor using the per-node residual

        self.update_displacement()
        self.update_temperature()

        # Print the normalized residual on the terminal

        tb.Res.display_residual()

        # Check if the convergence criterion has been reached

        return tb.Res.check()

    def transfer_dirichlet(self):
        '''
        Interpolate the solution from the solid to the fluid interface
        '''

        # The functions run only if their respective coupling is enabled

        tb.Interp.apply_displacement()
        tb.Interp.apply_temperature()

    def transfer_neumann(self):
        '''
        Interpolate the solution from the fluid to the solid interface
        '''

        # The functions run only if their respective coupling is enabled

        tb.Interp.apply_loading()
        tb.Interp.apply_heatflux()
