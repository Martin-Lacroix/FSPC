import numpy as np

# %% Displacement Norm Criterion

class Convergence(object):
    def __init__(self,param):

        self.epsilon = np.inf
        self.tol = param['tol']

    # Updates the displacment norm
    
    def update(self,res):

        norm = np.linalg.norm(res,axis=0)
        self.epsilon = np.linalg.norm(norm)
        
    # Checks the convergence

    def isVerified(self):

        if self.epsilon < self.tol: return True
        else: return False

# %% Time and Step Manager

class TimeStep(object):
    def __init__(self,param):

        self.time = 0
        self.factor = 2
        self.dt = param['dt']
        self.dtMax = param['dt']

    # Return the curent time frame

    def timeFrame(self):
        return self.time,self.time+self.dt
        
    # Update the time step

    def update(self,verified):

        if verified:

            self.time += self.dt
            self.dt = self.factor**(1/7)*self.dt
            if self.dt > self.dtMax: self.dt = self.dtMax

        else: self.dt = self.dt/self.factor
