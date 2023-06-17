from contextlib import redirect_stdout as stdout
from contextlib import redirect_stderr as stderr
from mpi4py.MPI import COMM_WORLD as CW
import collections
import numpy as np
import math, time
import fwkw

# %% Clock Dictionary and Empty Class

global clock
clock = collections.defaultdict(float)

class Undefined(object):
    def __getattribute__(self,_):
        raise Exception('The class has not been defined')
    
    def __bool__(self):
        return False

# %% Define Some Decorator Functions

def write_logs(func):
    def wrapper(*args,**kwargs):

        rank = str(CW.rank)
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
        self.minDt = 1e-9
        self.division = int(2)
        self.maxDt = self.dt = dt
        self.next = self.dtSave = dtSave

    def timeFrame(self):
        return self.time,self.time+self.dt

    # Update save time and export results if needed

    def updateSave(self,solver):

        if self.time >= self.next: solver.save()
        next = math.floor(self.time/self.dtSave)
        self.next = (next+1)*self.dtSave

    # Update the coupling time step

    def updateTime(self,verified):

        if not verified:
            
            self.dt /= self.division
            if self.dt < self.minDt:
                raise Exception('Reached minimal time step')

        else:

            self.time += self.dt
            self.dt = math.pow(self.division,1/7)*self.dt
            self.dt = min(self.dt,self.maxDt)

# %% MPI Process and Solvers

class Process(object):
    def __init__(self):

        self.rank = CW.rank
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

def printClock():

    global clock
    print('\n------------------------------------')
    print('Process {:.0f} : Time Stats'.format(CW.rank))
    print('------------------------------------\n')
    
    for fun,time in clock.items():
        print('{}{:.5f}'.format(fun.ljust(20),time))