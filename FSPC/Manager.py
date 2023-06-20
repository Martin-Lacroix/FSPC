import numpy as np
import math

# %% Coupling Time Step Manager

class TimeStep(object):
    def __init__(self,dt,dtSave):

        self.time = 0
        self.minDt = 1e-9
        self.division = int(2)
        self.maxDt = self.dt = dt
        self.next = self.dtSave = dtSave

    def nexTime(self):
        return self.time+self.dt

    # Update next save time and export results if needed

    def updateSave(self,solver):

        if self.time >= self.next: solver.save()
        next = math.floor(self.time/self.dtSave)
        self.next = (next+1)*self.dtSave

    # Update the current coupling time step

    def updateTime(self,verified):

        if not verified:
            
            self.dt /= self.division
            if self.dt < self.minDt:
                raise Exception('Reached minimal time step')

        else:

            self.time += self.dt
            self.dt = math.pow(self.division,1/7)*self.dt
            self.dt = min(self.dt,self.maxDt)

# %% Solution Convergence Manager

class Convergence(object):
    def __init__(self,tol):

        self.tol = tol
        self.epsilon = np.inf

    # Updates the displacment norm
    
    def update(self,res):

        norm = np.linalg.norm(res,axis=0)
        self.epsilon = np.linalg.norm(norm)
        
    # Checks the convergence

    def verified(self):

        if self.epsilon < self.tol: return True
        else: return False
