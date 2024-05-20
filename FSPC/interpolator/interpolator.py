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

        if tb.is_fluid():

            self.recv_pos = CW.recv(source=1, tag=1)
            CW.send(position, 1, tag=2)

        elif tb.is_solid():

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

        if tb.is_solid():

            recv = CW.recv(source=0, tag=3)
            tb.Solver.apply_loading(self.interpolate(recv))

        else: CW.send(tb.Solver.get_loading(), 1, tag=3)

    # Apply predicted displacement to the fluid

    @tb.only_mechanical
    def apply_displacement(self):

        if tb.is_fluid():

            recv = CW.recv(source=1, tag=4)
            tb.Solver.apply_displacement(self.interpolate(recv))

        else: CW.send(self.disp, 0, tag=4)

    # Apply actual heat flux to the solid

    @tb.only_thermal
    def apply_heatflux(self):

        if tb.is_solid():

            recv = CW.recv(source=0, tag=5)
            tb.Solver.apply_heatflux(self.interpolate(recv))

        else: CW.send(tb.Solver.get_heatflux(), 1, tag=5)

    # Apply predicted temperature to the fluid

    @tb.only_thermal
    def apply_temperature(self):

        if tb.is_fluid():

            recv = CW.recv(source=1, tag=6)
            tb.Solver.apply_temperature(self.interpolate(recv))

        else: CW.send(self.temp, 0, tag=6)

# |------------------------------------------|
# |   Update the Solver After Convergence    |
# |------------------------------------------|

    def update_solver(self):

        if tb.is_fluid():

            surface_mesh = CW.recv(source=1, tag=7)
            tb.Solver.update(surface_mesh)

        elif tb.is_solid():

            CW.send(tb.Solver.get_surface_mesh(), 0, tag=7)
            tb.Solver.update()
