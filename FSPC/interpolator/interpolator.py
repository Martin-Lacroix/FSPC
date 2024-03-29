from mpi4py.MPI import COMM_WORLD as CW
from ..general import toolbox as tb
import numpy as np

# |------------------------------------|
# |   Parent FSI Interpolator Class    |
# |------------------------------------|

class Interpolator(object):

    def initialize(self):

        position = tb.Solver.get_position()

        # Share the position vector between solvers

        if CW.rank == 0:

            self.recv_pos = CW.recv(source=1, tag=1)
            CW.send(position, 1, tag=2)

        elif CW.rank == 1:

            self.disp = np.copy(position)
            if tb.has_therm: self.temp = tb.Solver.get_temperature()

            CW.send(position, 0, tag=1)
            self.recv_pos = CW.recv(source=0, tag=2)

        # Compute the FS mesh interpolation matrix

        if hasattr(self, 'mapping'): self.mapping(position)

# |------------------------------------------|
# |   Communicate the Boundary Conditions    |
# |------------------------------------------|

    @tb.only_mechanical
    def apply_loading(self):

        if CW.rank == 1:

            recv = CW.recv(source=0, tag=3)
            tb.Solver.apply_loading(self.interpolate(recv))

        else: CW.send(tb.Solver.get_loading(), 1, tag=3)

    # Apply predicted displacement to the fluid

    @tb.only_mechanical
    def apply_displacement(self):

        if CW.rank == 0:

            recv = CW.recv(source=1, tag=4)
            tb.Solver.apply_displacement(self.interpolate(recv))

        else: CW.send(self.disp, 0, tag=4)

    # Apply actual heat flux to the solid

    @tb.only_thermal
    def apply_heatflux(self):

        if CW.rank == 1:

            recv = CW.recv(source=0, tag=5)
            tb.Solver.apply_heatflux(self.interpolate(recv))

        else: CW.send(tb.Solver.get_heatflux(), 1, tag=5)

    # Apply predicted temperature to the fluid

    @tb.only_thermal
    def apply_temperature(self):

        if CW.rank == 0:

            recv = CW.recv(source=1, tag=6)
            tb.Solver.apply_temperature(self.interpolate(recv))

        else: CW.send(self.temp, 0, tag=6)

# |---------------------------------------------|
# |   Predict the Solution for Next Coupling    |
# |---------------------------------------------|

    @tb.only_mechanical
    def predict_displacement(self, verified: bool):

        if not hasattr(self, 'prev_disp') or verified:

            self.prev_disp = np.copy(self.disp)
            self.velocity_disp = tb.Solver.get_velocity()
            self.disp += tb.Step.dt*self.velocity_disp

        else:

            self.disp = np.copy(self.prev_disp)
            self.disp += tb.Step.dt*self.velocity_disp

    # Predictor for the temparature coupling

    @tb.only_thermal
    def predict_temperature(self, verified: bool):

        if not hasattr(self, 'prev_temp') or verified:

            self.prev_temp = np.copy(self.temp)
            self.velocity_temp = tb.Solver.get_tempgrad()
            self.temp += tb.Step.dt*self.velocity_temp

        else:

            self.temp = np.copy(self.prev_temp)
            self.temp += tb.Step.dt*self.velocity_temp

# |------------------------------------------|
# |   Update the Solver After Convergence    |
# |------------------------------------------|

    def update_solver(self):

        if CW.rank == 0:

            polytope = CW.recv(source=1, tag=7)
            tb.Solver.update(polytope)

        elif CW.rank == 1:

            CW.send(tb.Solver.get_polytope(), 0, tag=7)
            tb.Solver.update()
