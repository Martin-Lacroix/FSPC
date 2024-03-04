from contextlib import redirect_stdout as stdout
from contextlib import redirect_stderr as stderr
from mpi4py.MPI import COMM_WORLD as CW
from . import Manager as ma
import time

# |------------------------------------|
# |   Empty Class Raising Exception    |
# |------------------------------------|

class Void(object):

    def __setattr__(self,*_):
        raise Exception('The class has not been defined')

    def __getattribute__(self,_):
        raise Exception('The class has not been defined')
    
    def __bool__(self):
        return False

# |--------------------------------------|
# |   Initialize the Global Variables    |
# |--------------------------------------|

global Step
Step = Void()

global Algo
Algo = Void()

global Interp
Interp = Void()

global Solver
Solver = Void()

global ResMech
ResMech = Void()

global ResTher
ResTher = Void()

# Convert solver prints to Python

global redirect

try:
    import pyStream
    redirect = pyStream.Redirect()
except: redirect = None

# Store the computation times of functions

global clock
import collections
clock = collections.defaultdict(float)

# |--------------------------------------|
# |   Define Some Decorator Functions    |
# |--------------------------------------|

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
        parent = args[0].__class__.__name__+' : '
        clock[parent+func.__name__] += time.time()-start

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

        global ResMech
        if ResMech: result = func(*args,**kwargs)
        else: result = None

        return result
    return wrapper

# Only accessed when thermal coupling

def conv_therm(func):
    def wrapper(*args,**kwargs):

        global ResTher
        if ResTher: result = func(*args,**kwargs)
        else: result = None

        return result
    return wrapper

# |------------------------------------|
# |   Initialize the Global Classes    |
# |------------------------------------|

def setStep(dt,dtSave):

    global Step
    Step = ma.TimeStep(dt,dtSave)
    return Step

def setAlgo(algorithm,*arg):

    global Algo
    Algo = algorithm(*arg)
    return Algo

def setInterp(interpolator,*arg):

    global Interp
    Interp = interpolator(*arg)
    return Interp

def setResMech(tol):

    global ResMech
    ResMech = ma.Residual(tol)
    return ResMech

def setResTher(tol):

    global ResTher
    ResTher = ma.Residual(tol)
    return ResTher

def simulate(endTime):

    global Algo
    return Algo.simulate(endTime)

# |----------------------------------------|
# |   Import and Initialize the Solvers    |
# |----------------------------------------|

@write_logs
def setSolver(pathF,pathS):

    global Solver

    if CW.rank == 0:

        from ..solver.Pfem3D import Pfem3D
        Solver = Pfem3D(pathF)

    if CW.rank == 1:

        from ..solver.Metafor import Metafor
        Solver = Metafor(pathS)

# |--------------------------------------------|
# |   Print the Summary of Computation Time    |
# |--------------------------------------------|

def printClock():

    global clock
    print('\n------------------------------------')
    print('Process {:.0f} : Time Stats'.format(CW.rank))
    print('------------------------------------\n')
    
    for fun,time in clock.items():
        print('{}{:.5f}'.format(fun.ljust(25),time))
