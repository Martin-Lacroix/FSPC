from contextlib import redirect_stdout as stdout
from contextlib import redirect_stderr as stderr
from mpi4py.MPI import COMM_WORLD as CW
import collections,time
import fwkw

# %% Empty Class Raising Exception

class Void(object):

    def __setattr__(self,*_):
        raise Exception('The class has not been defined')

    def __getattribute__(self,_):
        raise Exception('The class has not been defined')
    
    def __bool__(self):
        return False

# %% Initialize the Global Variables

global step
step = Void()

global interp
interp = Void()

global solver
solver = Void()

global convMech
convMech = Void()

global convTher
convTher = Void()

# Convert solver prints to Python

global redirect
redirect = fwkw.StdOutErr2Py()

global clock
clock = collections.defaultdict(float)

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

# Only accessed by the solid solver

def only_solid(func):
    def wrapper(*args,**kwargs):

        if CW.rank == 1: result = func(*args,**kwargs)
        else: result = None
        
        return result
    return wrapper

# Only accessed when mechanical coupling

def conv_mecha(func):
    def wrapper(*args,**kwargs):

        global convMech
        if convMech: result = func(*args,**kwargs)
        else: result = None

        return result
    return wrapper

# Only accessed when thermal coupling

def conv_therm(func):
    def wrapper(*args,**kwargs):

        global convTher
        if convTher: result = func(*args,**kwargs)
        else: result = None

        return result
    return wrapper

# %% Import Classes from Other Files

from . import Manager as ma
from . import Element as el

def getElement(nbrNod):

    if nbrNod == 2: return el.Line()
    if nbrNod == 3: return el.Triangle()
    if nbrNod == 4: return el.Quadrangle()

# %% Initialize the Global Class

def setStep(dt,dtSave):

    global step
    step = ma.TimeStep(dt,dtSave)
    return step

def setInterp(interpolator,*arg):

    global interp
    interp = interpolator(*arg)
    return interp

def setConvMech(tol):

    global convMech
    convMech = ma.Convergence(tol)
    return convMech

def setConvTher(tol):

    global convTher
    convTher = ma.Convergence(tol)
    return convTher

# %% Import and initialize the solvers

@write_logs
def setSolver(pathF,pathS):

    global solver

    if CW.rank == 0:

        from ..solver.Pfem3D import Pfem3D
        solver = Pfem3D(pathF)

    if CW.rank == 1:

        from ..solver.Metafor import Metafor
        solver = Metafor(pathS)

# %% Print the Computation Times

def printClock():

    global clock
    print('\n------------------------------------')
    print('Process {:.0f} : Time Stats'.format(CW.rank))
    print('------------------------------------\n')
    
    for fun,time in clock.items():
        print('{}{:.5f}'.format(fun.ljust(20),time))