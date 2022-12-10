from contextlib import redirect_stdout as stdout
from mpi4py import MPI
import collections
import numpy as np
import time
import fwkw

# Dictionary of computation time

global clock
clock = collections.defaultdict(float)

# %% Define Decorator Functions

def write_logs(func):
    def wrapper(*args,**kwargs):

        rank = str(MPI.COMM_WORLD.rank)
        with open('solver_'+rank+'.dat','a') as file:
            with stdout(file): result = func(*args,**kwargs)
        
        return result
    return wrapper

# Measure the computation time

def compute_time(func):
    def wrapper(*args,**kwargs):

        global clock
        start = time.time()
        result = func(*args,**kwargs)
        clock[func.__name__] += time.time()-start
        
        return result
    return wrapper

# %% Displacement Norm Criterion

class Convergence(object):
    def __init__(self,tol):

        self.tol = tol
        self.epsilon = np.inf

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
    def __init__(self,dt):

        self.time = 0
        self.factor = int(2)
        self.max = self.dt = dt

    # Return the curent time frame

    def timeFrame(self):
        return self.time,self.time+self.dt
        
    # Update the time step

    def update(self,verified):

        if verified:

            self.time += self.dt
            self.dt = self.factor**(1/7)*self.dt
            if self.dt > self.max: self.dt = self.max

        else: self.dt = self.dt/self.factor

# %% MPI Process and Solvers

class Process(object):
    def __init__(self):

        self.com = MPI.COMM_WORLD
        self.rank = MPI.COMM_WORLD.rank
        self.redirect = fwkw.StdOutErr2Py()

    # Import and initialize the solvers

    @write_logs
    def getSolver(self,pathF,pathS):

        if self.rank == 0:

            from .solver.Pfem3D import Pfem3D
            return Pfem3D(pathF)

        if self.rank == 1:

            from .solver.Metafor import Metafor
            return Metafor(pathS)

# %% Print the Computation Times

def printClock(com):

    global clock
    print('\n------------------------------------')
    print('Process {:.0f} : Time Stats'.format(com.rank))
    print('------------------------------------\n')
    for I,T in clock.items(): print('{}{:.5f}'.format(I.ljust(20),T))