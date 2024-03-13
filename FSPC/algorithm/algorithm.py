from mpi4py.MPI import COMM_WORLD as CW
from ..general import toolbox as tb
import numpy as np

# |---------------------------------|
# |   Parent FSI Algorithm Class    |
# |---------------------------------|

class Algorithm(object):
    def __init__(self):

        self.has_run = False

# |-------------------------------------------|
# |   Start the Fluid-Structure Simulation    |
# |-------------------------------------------|

    @tb.compute_time
    def simulate(self, end_time: float):

        verified = True
        tb.Solver.save()

        # Main loop on the FSI coupling time steps

        while tb.Step.time < end_time:

            tb.Interp.initialize()
            self.display_time_step()
            self.reset_convergence()

            # Main loop on the FSI coupling iterations

            self.compute_predictor(verified)
            verified = self.coupling_algorithm()
            tb.Step.update_time(verified)

            # Update the solvers for the next time step

            if verified:

                tb.Interp.update_solver()
                tb.Step.update_exporter()
                self.has_run = False

            else: self.way_back(); continue

        # End of the FSI simulation

        CW.barrier()
        tb.Solver.exit()

# |-----------------------------------------|
# |   Run and Restore the Solver Backups    |
# |-----------------------------------------|

    def run_fluid(self):

        if CW.rank == 0:

            self.has_run = True
            verified = tb.Solver.run()

        else: verified = None
        return CW.bcast(verified, root=0)

    def run_solid(self):

        if CW.rank == 1:

            self.has_run = True
            verified = tb.Solver.run()

        else: verified = None
        return CW.bcast(verified, root=1)

    # Reset the solvers to their last backup state

    @tb.write_logs
    @tb.compute_time
    def way_back(self):

        if self.has_run: tb.Solver.way_back()
        self.has_run = False

# |--------------------------------------------|
# |   Interpolator Functions and Relaxation    |
# |--------------------------------------------|

    @tb.only_solid
    def compute_predictor(self, verified: bool):

        tb.Interp.predict_temperature(verified)
        tb.Interp.predict_displacement(verified)

    @tb.only_solid
    def reset_convergence(self):

        if tb.ResMech: tb.ResMech.reset()
        if tb.ResTher: tb.ResTher.reset()

    # Update the predicted interface solution

    @tb.only_solid
    @tb.compute_time
    def relaxation(self):

        self.compute_residual()
        self.update_displacement()
        self.update_temperature()
        self.display_residual()

        # Check for coupling convergence

        verified = list()
        if tb.ResMech: verified.append(tb.ResMech.verified())
        if tb.ResTher: verified.append(tb.ResTher.verified())
        return np.all(verified)

# |------------------------------------|
# |   Transfer and Update Functions    |
# |------------------------------------|

    def compute_residual(self):

        if tb.ResMech:

            disp = tb.Solver.get_position()
            tb.ResMech.update_res(disp, tb.Interp.disp)

        if tb.ResTher:

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

        if tb.ResMech:

            iter = '[{:.0f}]'.format(self.iteration)
            eps = 'Residual Mech : {:.3e}'.format(tb.ResMech.epsilon)
            print(iter, eps)

        if tb.ResTher:

            iter = '[{:.0f}]'.format(self.iteration)
            eps = 'Residual Ther : {:.3e}'.format(tb.ResTher.epsilon)
            print(iter, eps)

    @tb.only_solid
    def display_time_step(self):

        L = '\n------------------------------------------'
        time_step = 'Time Step : {:.3e}'.format(tb.Step.dt)
        time = '\nTime : {:.3e}'.format(tb.Step.time).ljust(20)
        print(L, time, time_step, L)
