from ..general import toolbox as tb
import numpy as np

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

            # Build the interpolation matrices on the current interface

            tb.Interp.initialize()

            # Reset the residual and predict the equilibrium solution

            self.reset_convergence()
            self.compute_predictor()

            # Perform the coupling iterations and update the time step

            self.verified = self.coupling_algorithm()
            tb.Step.update_time(self.verified)

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

        tb.Interp.predict_temperature(self.verified)
        tb.Interp.predict_displacement(self.verified)

    @tb.only_solid
    def reset_convergence(self):
        '''
        Reset the residual attributes to their default values
        '''

        # Call the class only if it has been enabled by the user

        if tb.has_mecha: tb.ResMech.reset()
        if tb.has_therm: tb.ResTher.reset()

    @tb.only_solid
    @tb.compute_time
    def relaxation(self):
        '''
        Compute the predicted solution at the solid interface
        '''

        # Compute the residual between the predictor and Metafor

        self.compute_residual()

        # Update the predictor using the per-node residual

        self.update_displacement()
        self.update_temperature()

        # Print the normalized residual on the terminal

        self.display_residual()

        # Check if the convergence criterion has been reached

        ok_list = list()
        if tb.has_mecha: ok_list.append(tb.ResMech.check())
        if tb.has_therm: ok_list.append(tb.ResTher.check())

        # Return true only if both couplings have converged

        return np.all(ok_list)

    def compute_residual(self): # ???
        '''
        Compute the residual of the solution at the solid interface
        '''

        if tb.has_mecha:

            # Difference between the displacement predictor and Metafor

            disp = tb.Solver.get_position()
            tb.ResMech.update_res(disp, tb.Interp.disp)

        if tb.has_therm:

            # Difference between the temperature predictor and Metafor

            temp = tb.Solver.get_temperature()
            tb.ResTher.update_res(temp, tb.Interp.temp)

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

    def display_residual(self):
        '''
        Print the current state of the convergence criterion
        '''

        if tb.has_mecha:

            # Print the normalized residual for the mechanical coupling

            eps = 'Residual Mech : {:.3e}'.format(tb.ResMech.epsilon)
            print('[{:.0f}]'.format(self.iteration), eps)

        if tb.has_therm:

            # Print the normalized residual for the thermal coupling

            eps = 'Residual Ther : {:.3e}'.format(tb.ResTher.epsilon)
            print('[{:.0f}]'.format(self.iteration), eps)
