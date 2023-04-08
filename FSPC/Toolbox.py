from contextlib import redirect_stdout as stdout
from contextlib import redirect_stderr as stderr
from mpi4py import MPI
import collections
import numpy as np
import math, time
import fwkw

# Dictionary of computation time

global clock
clock = collections.defaultdict(float)

# %% Define Decorator Functions

def write_logs(func):
    def wrapper(*args,**kwargs):

        rank = str(MPI.COMM_WORLD.rank)
        with open('solver_'+rank+'.dat','a') as output:
            with stderr(output), stdout(output):
                result = func(*args,**kwargs)
        
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

# %% Interface Data Norm Criterion

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

# %% Coupling Time Step Manager

class TimeStep(object):
    def __init__(self,dt,dtSave):

        self.time = 0
        self.factor = int(2)
        self.maximum = self.dt = dt
        self.next = self.dtSave = dtSave

    def timeFrame(self):
        return self.time,self.time+self.dt

    # Update and return if save is required

    def mustSave(self):

        output = (self.time >= self.next)
        next = math.floor(self.time/self.dtSave)
        self.next = (next+1)*self.dtSave
        return output
        
    # Update the coupling time step

    def update(self,verified):

        if not verified: self.dt /= self.factor
        else:

            self.time += self.dt
            self.dt = math.pow(self.factor,1/7)*self.dt
            self.dt = min(self.dt,self.maximum)

# %% MPI Process and Solvers

class Process(object):
    def __init__(self):

        self.com = MPI.COMM_WORLD
        self.redirect = fwkw.StdOutErr2Py()

    # Import and initialize the solvers

    @write_logs
    def getSolver(self,pathF,pathS):

        if self.com.rank == 0:

            from .solver.Pfem3D import Pfem3D
            return Pfem3D(pathF)

        if self.com.rank == 1:

            from .solver.Metafor import Metafor
            return Metafor(pathS)

# %% Print the Computation Times

def printClock():

    global clock
    rank = MPI.COMM_WORLD.rank

    print('\n------------------------------------')
    print('Process {:.0f} : Time Stats'.format(rank))
    print('------------------------------------\n')
    
    for fun,time in clock.items():
        print('{}{:.5f}'.format(fun.ljust(20),time))