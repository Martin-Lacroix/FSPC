from mpi4py.MPI import COMM_WORLD as CW
from ..general import toolbox as tb
import numpy as np

# Base fluid-structure interpolation class

class Interpolator(object):

    def initialize(self):
        '''
        Initialize the base fluid-structure interpolation class
        '''

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

        # Compute the fluid-structure mesh interpolation matrix

        if hasattr(self, 'mapping'): self.mapping(position)

    @tb.only_mechanical
    def apply_loading(self):
        '''
        Apply the loading from the fluid to the solid interface
        '''

        if tb.is_solid():

            recv = CW.recv(source=0, tag=3)
            tb.Solver.apply_loading(self.interpolate(recv))

        else: CW.send(tb.Solver.get_loading(), 1, tag=3)

    @tb.only_mechanical
    def apply_displacement(self):
        '''
        Apply the displacement from the solid to the fluid interface
        '''

        if tb.is_fluid():

            recv = CW.recv(source=1, tag=4)
            tb.Solver.apply_displacement(self.interpolate(recv))

        else: CW.send(self.disp, 0, tag=4)

    @tb.only_thermal
    def apply_heatflux(self):
        '''
        Apply the heat flux from the fluid to the solid interface
        '''

        if tb.is_solid():

            recv = CW.recv(source=0, tag=5)
            tb.Solver.apply_heatflux(self.interpolate(recv))

        else: CW.send(tb.Solver.get_heatflux(), 1, tag=5)

    @tb.only_thermal
    def apply_temperature(self):
        '''
        Apply the temperature from the solid to the fluid interface
        '''

        if tb.is_fluid():

            recv = CW.recv(source=1, tag=6)
            tb.Solver.apply_temperature(self.interpolate(recv))

        else: CW.send(self.temp, 0, tag=6)

    @tb.only_mechanical
    def predict_displacement(self, verified: bool):
        '''
        Predict the future displacement of the solid interface
        '''

        if not hasattr(self, 'prev_disp') or verified:

            self.prev_disp = np.copy(self.disp)
            self.velocity_disp = tb.Solver.get_velocity()
            self.disp += tb.Step.dt*self.velocity_disp

        else:

            self.disp = np.copy(self.prev_disp)
            self.disp += tb.Step.dt*self.velocity_disp

    @tb.only_thermal
    def predict_temperature(self, verified: bool):
        '''
        Predict the future temperature of the solid interface
        '''

        if not hasattr(self, 'prev_temp') or verified:

            self.prev_temp = np.copy(self.temp)
            self.velocity_temp = tb.Solver.get_tempgrad()
            self.temp += tb.Step.dt*self.velocity_temp

        else:

            self.temp = np.copy(self.prev_temp)
            self.temp += tb.Step.dt*self.velocity_temp
