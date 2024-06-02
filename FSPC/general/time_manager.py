from mpi4py.MPI import COMM_WORLD as CW
from . import toolbox as tb
import math, sys

# |------------------------------------------|
# |   Disk Exporter and Time Step Manager    |
# |------------------------------------------|

class TimeStep(tb.Frozen):
    def __init__(self, dt: float, dt_save: float):

        self.__setattr__('dt', dt)
        self.__setattr__('time', 0)

        # Time step for writing results on the disk

        self.__setattr__('dt_save', dt_save)
        self.__setattr__('next_save', dt_save)

        # Maximum and minimum coupling time step

        self.__setattr__('max_dt', dt)
        self.__setattr__('min_dt', 1e-9)

        tb.Frozen.__init__(self)

    def next_time(self):
        return self.time+self.dt

    # Update next save time and export results if needed

    def update_exporter(self):

        if self.time >= self.next_save: tb.Solver.save()
        next_save = math.floor(self.time/self.dt_save)
        self.next_save = (next_save+1)*self.dt_save

    # Update the current coupling time step

    def update_time(self, verified: bool):

        if not verified and (self.dt < self.min_dt):

            CW.Barrier()
            if tb.is_solid(): print('Reached minimal time step')
            sys.exit()

        elif not verified: self.dt /= 2

        else:

            self.time += self.dt
            self.dt = math.pow(2, 1/7)*self.dt
            self.dt = min(self.dt, self.max_dt)

# |----------------------------------|
# |   Print the Current Time Step    |
# |----------------------------------|

    @tb.only_solid
    def display_time_step(self):

        current = 'Time : {:.3e}'.format(self.time).ljust(20)
        print('\n------------------------------------------')
        print(current, 'Time Step : {:.3e}'.format(self.dt))
        print('------------------------------------------')
