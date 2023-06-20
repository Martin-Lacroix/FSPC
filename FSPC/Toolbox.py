from contextlib import redirect_stdout as stdout
from contextlib import redirect_stderr as stderr
from mpi4py.MPI import COMM_WORLD as CW
from . import Manager as mg
import collections,time
import fwkw

# %% Define Some Global Variables

global redirect
redirect = fwkw.StdOutErr2Py()

global clock
clock = collections.defaultdict(float)

# %% Print the Output in Log File

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

# %% Only Accessed by Rank 0 Fluid Solver

def only_fluid(func):
    def wrapper(*args,**kwargs):

        if CW.rank == 0: result = func(*args,**kwargs)
        else: result = None

        return result
    return wrapper

# Only accessed by rank 1 solid solver

def only_solid(func):
    def wrapper(*args,**kwargs):

        if CW.rank == 1: result = func(*args,**kwargs)
        else: result = None
        
        return result
    return wrapper

# %% Only Accessed when Mechanical Coupling

def only_mecha(func):
    def wrapper(*args,**kwargs):

        if mg.convMecha: result = func(*args,**kwargs)
        else: result = None

        return result
    return wrapper

# Only accessed when thermal coupling

def only_therm(func):
    def wrapper(*args,**kwargs):

        if mg.convTherm: result = func(*args,**kwargs)
        else: result = None

        return result
    return wrapper

# %% Import and initialize the solvers

@write_logs
def getSolver(pathF,pathS):

    if CW.rank == 0:

        from .solver.Pfem3D import Pfem3D
        return Pfem3D(pathF)

    if CW.rank == 1:

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