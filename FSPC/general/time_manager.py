from . import toolbox as tb
import math, sys

# Disk exporter and time step manager class

class TimeStep(object):
    def __init__(self, dt: float, dt_save: float):
        '''
        Initialize the disk exporter and time step manager class
        '''

        self.time = 0
        self.min_dt = 1e-9

        self.max_dt = self.dt = dt
        self.next = self.dt_save = dt_save

    def next_time(self):
        '''
        Return the physical time at the end of the current step
        '''

        return self.time+self.dt

    def update_exporter(self):
        '''
        Update the time step for the disk exporter
        '''

        if self.time >= self.next: tb.Solver.save()
        next = math.floor(self.time/self.dt_save)
        self.next = (next+1)*self.dt_save

    def update_time(self, verified: bool):
        '''
        Update the time step for the coupling algorithm
        '''

        if not verified and (self.dt < self.min_dt):

            tb.CW.Barrier()
            if tb.is_solid(): print('Reached minimal time step')
            sys.exit()

        elif not verified: self.dt /= 2

        else:

            self.time += self.dt
            self.dt = math.pow(2, 1/7)*self.dt
            self.dt = min(self.dt, self.max_dt)

    @tb.only_solid
    def display_time_step(self):
        '''
        Print the current time step and physical time
        '''

        current = 'Time : {:.3e}'.format(self.time).ljust(20)
        print('\n------------------------------------------')
        print(current, 'Time Step : {:.3e}'.format(self.dt))
        print('------------------------------------------')
