from contextlib import redirect_stdout as stdout
from contextlib import redirect_stderr as stderr
from mpi4py.MPI import COMM_WORLD as CW
from typing import Callable
import time

# |--------------------------------------|
# |   Initialize the Global Variables    |
# |--------------------------------------|

has_mecha = False
has_therm = False

# Convert solver prints to Python

try:
    import python_stream
    redirect = python_stream.Redirect()
except: redirect = None

# Store the computation times of functions

import collections
clock = collections.defaultdict(float)

# |--------------------------------------|
# |   Define Some Decorator Functions    |
# |--------------------------------------|

def write_logs(function: Callable):
    def wrapper(*args):

        rank = str(CW.rank)
        with open('solver_'+rank+'.dat', 'a') as output:
            with stderr(output), stdout(output):
                return function(*args)

    return wrapper

# Measure the computation time of functions

def compute_time(function: Callable):
    def wrapper(*args):

        start = time.time()
        result = function(*args)
        parent = args[0].__class__.__name__+' : '
        clock[parent+function.__name__] += time.time()-start

        return result
    return wrapper

# Function called by the solid solver

def only_solid(function: Callable):
    def wrapper(*args):

        if CW.rank == 1: return function(*args)

    return wrapper

# Function called when mechanical coupling

def only_mechanical(function: Callable):
    def wrapper(*args):

        if has_mecha: return function(*args)

    return wrapper

# Function called when thermal coupling

def only_thermal(function: Callable):
    def wrapper(*args):

        if has_therm: return function(*args)

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

    global ResMech, has_mecha

    ResMech = residual
    has_mecha = True

def set_thermal_res(residual: object):

    global ResTher, has_therm

    ResTher = residual
    has_therm = True

# |----------------------------------------|
# |   Import and Initialize the Solvers    |
# |----------------------------------------|

@write_logs
def init_solver(path_F: str, path_S: str):

    global Solver

    if CW.rank == 0:

        from ..solver.pfem_3D import PFEM3D
        Solver = PFEM3D(path_F)

    elif CW.rank == 1:

        from ..solver.metafor import Metafor
        Solver = Metafor(path_S)

    return Solver

# |--------------------------------------------|
# |   Print the Summary of Computation Time    |
# |--------------------------------------------|

def print_clock():

    print('\n------------------------------------')
    print('Process {:.0f} : Time Stats'.format(CW.rank))
    print('------------------------------------\n')

    for key, value in clock.items():
        print('{}{:.5f}'.format(key.ljust(25), value))
