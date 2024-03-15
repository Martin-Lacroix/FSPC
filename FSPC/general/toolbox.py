from contextlib import redirect_stdout as stdout
from contextlib import redirect_stderr as stderr
from mpi4py.MPI import COMM_WORLD as CW
import time

# |------------------------------------|
# |   Empty Class Raising Exception    |
# |------------------------------------|

class Void(object):

    def __setattr__(self, name: str, _):
        raise Exception('Set {'+name+'} of empty class')

    def __getattribute__(self, name: str):
        raise Exception('Get {'+name+'} of empty class')

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
    import python_stream
    redirect = python_stream.Redirect()
except: redirect = Void()

# Store the computation times of functions

global clock
import collections
clock = collections.defaultdict(float)

# |--------------------------------------|
# |   Define Some Decorator Functions    |
# |--------------------------------------|

def write_logs(function: object):
    def wrapper(*args, **kwargs):

        rank = str(CW.rank)
        with open('solver_'+rank+'.dat', 'a') as output:
            with stderr(output), stdout(output):
                result = function(*args, **kwargs)

        return result
    return wrapper

# Measure the computation time

def compute_time(function: object):
    def wrapper(*args, **kwargs):

        global clock
        start = time.time()
        result = function(*args, **kwargs)
        parent = args[0].__class__.__name__+' : '
        clock[parent+function.__name__] += time.time()-start

        return result
    return wrapper

# Only accessed by the solid solver

def only_solid(function: object):
    def wrapper(*args, **kwargs):

        if CW.rank == 1: result = function(*args, **kwargs)
        else: result = None

        return result
    return wrapper

# Only accessed when mechanical coupling

def only_mechanical(function: object):
    def wrapper(*args, **kwargs):

        global ResMech
        if ResMech: result = function(*args, **kwargs)
        else: result = None

        return result
    return wrapper

# Only accessed when thermal coupling

def only_thermal(function: object):
    def wrapper(*args, **kwargs):

        global ResTher
        if ResTher: result = function(*args, **kwargs)
        else: result = None

        return result
    return wrapper

# |------------------------------------|
# |   Initialize the Global Classes    |
# |------------------------------------|

def set_time_step(step_manager: object):

    global Step
    Step = step_manager

def set_algorithm(algorithm: object):

    global Algo
    Algo = algorithm

def set_interpolator(interpolator: object):

    global Interp
    Interp = interpolator

def set_mechanical_res(residual: object):

    global ResMech
    ResMech = residual

def set_thermal_res(residual: object):

    global ResTher
    ResTher = residual

# |----------------------------------------|
# |   Import and Initialize the Solvers    |
# |----------------------------------------|

@write_logs
def init_solver(path_F: str, path_S: str):

    global Solver

    if CW.rank == 0:

        from ..solver.pfem_3D import PFEM3D
        Solver = PFEM3D(path_F)
        return Solver

    elif CW.rank == 1:

        from ..solver.metafor import Metafor
        Solver = Metafor(path_S)
        return Solver

# |--------------------------------------------|
# |   Print the Summary of Computation Time    |
# |--------------------------------------------|

def print_clock():

    global clock
    print('\n------------------------------------')
    print('Process {:.0f} : Time Stats'.format(CW.rank))
    print('------------------------------------\n')

    for fun, time in clock.items():
        print('{}{:.5f}'.format(fun.ljust(25), time))
