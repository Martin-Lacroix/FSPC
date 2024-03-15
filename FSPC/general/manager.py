from . import toolbox as tb
import numpy as np
import math

# |---------------------------------|
# |   Coupling Time Step Manager    |
# |---------------------------------|

class TimeStep(object):
    def __init__(self, dt: float, dt_save: float):

        self.time = 0
        self.division = int(2)
        self.max_dt = self.dt = dt
        self.next = self.dt_save = dt_save

    def next_time(self):
        return self.time+self.dt

    # Update next save time and export results if needed

    def update_exporter(self):

        if self.time >= self.next: tb.Solver.save()
        next = math.floor(self.time/self.dt_save)
        self.next = (next+1)*self.dt_save

    # Update the current coupling time step

    def update_time(self, verified: bool):

        if not verified:

            self.dt /= self.division
            if self.dt < 1e-9: raise Exception('Reached minimal time step')

        else:

            self.time += self.dt
            self.dt = math.pow(self.division, 1/7)*self.dt
            self.dt = min(self.dt, self.max_dt)

# |--------------------------------|
# |   Solution Residual Manager    |
# |--------------------------------|

class Residual(object):
    def __init__(self, tol: float):

        self.tol = tol
        self.reset()

    def delta_res(self):
        return self.residual-self.prev_res

    # Reset all the convergence indicators

    def reset(self):

        self.prev_res = None
        self.residual = None
        self.epsilon = np.inf

    # Update the current and previous residual

    def update_res(self, result: np.ndarray, prediction: np.ndarray):

        self.prev_res = np.copy(self.residual)
        self.residual = result-prediction

        res = np.linalg.norm(self.residual, axis=0)
        den = np.linalg.norm(result, axis=0)

        res = res/(den+self.tol)
        self.epsilon = np.linalg.norm(res)

    # Check if the convergence criterion is verified

    def check(self):

        if self.epsilon < self.tol: return True
        else: return False
    