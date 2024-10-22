from . import toolbox as tb
import math, sys

# Disk exporter and time step manager class

class TimeStep(tb.Static):
    def __init__(self, dt: float, dt_save: float):
        '''
        Initialize the disk exporter and time step manager class
        '''

        object.__setattr__(self, 'time', 0)
        object.__setattr__(self, 'min_dt', 1e-9)

        # Time step and maximum for the fluid-structure simulation

        object.__setattr__(self, 'dt', dt)
        object.__setattr__(self, 'max_dt', dt)

        # Time step and first checkpoint for exporting on the disk

        object.__setattr__(self, 'next', dt_save)
        object.__setattr__(self, 'dt_save', dt_save)

    def update_exporter(self):
        '''
        Update the time step for the disk exporter
        '''

        # Export the solution if the checkpoint has been reached

        if self.time >= self.next: tb.Solver.save()

        # Update the next solution export checkpoint with dt_save

        next = math.floor(self.time/self.dt_save)
        self.next = (next+1)*self.dt_save

    def update_time(self):
        '''
        Update the time step for the coupling algorithm
        '''

        # The coupling did not converge the minimal time step is reached

        if not tb.Algo.verified and (self.dt < self.min_dt):

            # Wait for all processes and terminate the simulation

            tb.com.Barrier()
            if tb.is_solid(): print('Reached minimal time step')
            sys.exit()

        # Reduce the time step if the coupling did not converge 

        elif not tb.Algo.verified: self.dt /= 2

        # Increase the time step if the coupling has converged

        else:

            self.time += self.dt
            self.dt = math.pow(2, 1/7)*self.dt

            # Prevent the time step to increase above the maximum

            self.dt = min(self.dt, self.max_dt)

    @tb.only_solid
    def display_time_step(self):
        '''
        Print the current time step and physical time
        '''

        # Use a scientific notation with a fixed number of digits

        current_time = f'Time : {self.time:.3e}'.ljust(20)
        print('\n------------------------------------------')
        print(current_time, f'Time Step : {self.dt:.3e}')
        print('------------------------------------------')
