from ..general import toolbox as tb
import numpy as np

# |---------------------------------|
# |   Parent FSI Algorithm Class    |
# |---------------------------------|

class Algorithm(object):

    @tb.compute_time
    def simulate(self, end_time: float):

        self.verified = False
        if hasattr(self, 'initialize'): self.initialize()
        tb.Solver.save()

        # Main loop on the FSI coupling time steps

        while tb.Step.time < end_time:

            tb.Interp.initialize()
            tb.Step.display_time_step()
            self.reset_convergence()

            # Main loop on the FSI coupling iterations

            self.compute_predictor()
            self.verified = self.coupling_algorithm()
            tb.Step.update_time(self.verified)

            # Update the solvers for the next time step

            if self.verified:

                tb.Interp.update_solver()
                tb.Step.update_exporter()

# |--------------------------------------------|
# |   Interpolator Functions and Relaxation    |
# |--------------------------------------------|

    @tb.only_solid
    def compute_predictor(self):

        tb.Interp.predict_temperature(self.verified)
        tb.Interp.predict_displacement(self.verified)

    @tb.only_solid
    def reset_convergence(self):

        if tb.has_mecha: tb.ResMech.reset()
        if tb.has_therm: tb.ResTher.reset()

    # Update the predicted interface solution

    @tb.only_solid
    @tb.compute_time
    def relaxation(self):

        self.compute_residual()
        self.update_displacement()
        self.update_temperature()
        self.display_residual()

        # Check for coupling convergence

        ok_list = list()
        if tb.has_mecha: ok_list.append(tb.ResMech.check())
        if tb.has_therm: ok_list.append(tb.ResTher.check())
        return np.all(ok_list)

# |------------------------------------|
# |   Transfer and Update Functions    |
# |------------------------------------|

    def compute_residual(self):

        if tb.has_mecha:

            disp = tb.Solver.get_position()
            tb.ResMech.update_res(disp, tb.Interp.disp)

        if tb.has_therm:

            temp = tb.Solver.get_temperature()
            tb.ResTher.update_res(temp, tb.Interp.temp)

    # Transfer Dirichlet data Solid to Fluid

    def transfer_dirichlet(self):

        tb.Interp.apply_displacement()
        tb.Interp.apply_temperature()

    # Transfer Neumann data Fluid to Solid

    def transfer_neumann(self):

        tb.Interp.apply_loading()
        tb.Interp.apply_heatflux()

# |------------------------------------|
# |   Print Convergence Information    |
# |------------------------------------|

    def display_residual(self):

        if tb.has_mecha:

            eps = 'Residual Mech : {:.3e}'.format(tb.ResMech.epsilon)
            print('[{:.0f}]'.format(self.iteration), eps)

        if tb.has_therm:

            eps = 'Residual Ther : {:.3e}'.format(tb.ResTher.epsilon)
            print('[{:.0f}]'.format(self.iteration), eps)

