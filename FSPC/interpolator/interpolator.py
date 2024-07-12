from mpi4py.MPI import COMM_WORLD as CW
from ..general import toolbox as tb
import numpy as np

# Base fluid-structure interpolation class

class Interpolator(tb.Static):

    def initialize(self):
        '''
        Initialize the base fluid-structure interpolation class
        '''

        position = tb.Solver.get_position()

        # Previous solution used for computing the residual

        object.__setattr__(self, 'prev_disp', np.ndarray(0))
        object.__setattr__(self, 'prev_temp', np.ndarray(0))

        # Previous velocity used for the first predictor

        object.__setattr__(self, 'velocity_disp', np.ndarray(0))
        object.__setattr__(self, 'velocity_temp', np.ndarray(0))

        # Share the position vector between the solvers

        if tb.is_fluid():

            object.__setattr__(self, 'recv_pos', CW.recv(source=1, tag=1))
            CW.send(position, 1, tag=2)

        elif tb.is_solid():

            # The displacement is actually the solid position predictor

            CW.send(position, 0, tag=1)
            object.__setattr__(self, 'disp', position)
            object.__setattr__(self, 'recv_pos', CW.recv(source=0, tag=2))

            # Also initialize the temperature in thermal coupling

            if tb.has_therm:
                object.__setattr__(self, 'temp', tb.Solver.get_temperature())

        # Compute the fluid-structure mesh interpolation matrix

        self.mapping(position)

    @tb.only_mechanical
    def apply_loading(self):
        '''
        Apply the loading from the fluid to the solid interface
        '''

        if tb.is_solid():

            # Recieve the interface stress tensor from the fluid

            recv = CW.recv(source=0, tag=3)
            tb.Solver.apply_loading(self.interpolate(recv))

        # Send the interface stress tensor to the solid solver

        else: CW.send(tb.Solver.get_loading(), 1, tag=3)

    @tb.only_mechanical
    def apply_displacement(self):
        '''
        Apply the displacement from the solid to the fluid interface
        '''

        if tb.is_fluid():

            # Recieve the new interface position from the solid

            recv = CW.recv(source=1, tag=4)
            tb.Solver.apply_displacement(self.interpolate(recv))

        # Send the new interface position to the fluid solver

        else: CW.send(self.disp, 0, tag=4)

    @tb.only_thermal
    def apply_heatflux(self):
        '''
        Apply the heat flux from the fluid to the solid interface
        '''

        if tb.is_solid():

            # Recieve the interface heat flux from the fluid

            recv = CW.recv(source=0, tag=5)
            tb.Solver.apply_heatflux(self.interpolate(recv))

        # Send the interface heat flux to the solid solver

        else: CW.send(tb.Solver.get_heatflux(), 1, tag=5)

    @tb.only_thermal
    def apply_temperature(self):
        '''
        Apply the temperature from the solid to the fluid interface
        '''

        if tb.is_fluid():

            # Recieve the new interface temperature from the solid

            recv = CW.recv(source=1, tag=6)
            tb.Solver.apply_temperature(self.interpolate(recv))

        # Send the new interface temperature to the fluid solver

        else: CW.send(self.temp, 0, tag=6)

    @tb.only_mechanical
    def predict_displacement(self, verified: bool):
        '''
        Predict the future displacement of the solid interface
        '''

        # If first time step or if the equilibrium has been reached

        if not self.prev_disp.size or verified:

            # Update the previous solution with the current one

            self.prev_disp = np.copy(self.disp)
            self.velocity_disp = tb.Solver.get_velocity()

            # Predict the equilibrium position at the next time step

            self.disp += tb.Step.dt*self.velocity_disp

        else:

            # Predict from the previous equilibrium position

            self.disp = np.copy(self.prev_disp)
            self.disp += tb.Step.dt*self.velocity_disp

    @tb.only_thermal
    def predict_temperature(self, verified: bool):
        '''
        Predict the future temperature of the solid interface
        '''

        # If first time step or if the equilibrium has been reached

        if not self.prev_temp.size or verified:

            # Update the previous solution with the current one

            self.prev_temp = np.copy(self.temp)
            self.velocity_temp = tb.Solver.get_temperature_rate()

            # Predict the equilibrium temperature at the next time step

            self.temp += tb.Step.dt*self.velocity_temp

        else:

            # Predict from the previous equilibrium temperature

            self.temp = np.copy(self.prev_temp)
            self.temp += tb.Step.dt*self.velocity_temp
