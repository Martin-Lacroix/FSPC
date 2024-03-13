from contextlib import redirect_stdout as stdout
from contextlib import redirect_stderr as stderr
from mpi4py.MPI import COMM_WORLD as CW
import time

# |------------------------------------|
# |   Empty Class Raising Exception    |
# |------------------------------------|

class Void(object):

    def __setattr__(self, *_: tuple):
        raise Exception('The class has not been defined')

    def __getattribute__(self, _: str):
        raise Exception('The class has not been defined')

    def __bool__(self):
        return False

# |--------------------------------------|
# |   Initialize the Global Variables    |
# |--------------------------------------|

global Step
Step: object = Void()

global Algo
Algo: object = Void()

global Interp
Interp: object = Void()

global Solver
Solver: object = Void()

global ResMech
ResMech: object = Void()

global ResTher
ResTher: object = Void()

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

def write_logs(func: object):
    def wrapper(*args: tuple, **kwargs: dict):

        rank = str(CW.rank)
        with open('solver_' + rank + '.dat', 'a') as output:
            with stderr(output), stdout(output):
                result = func(*args, **kwargs)

        return result
    return wrapper

# Measure the computation time

def compute_time(func: object):
    def wrapper(*args: tuple, **kwargs: dict):

        global clock
        start = time.time()
        result = func(*args, **kwargs)
        parent = args[0].__class__.__name__ + ' : '
        clock[parent + func.__name__] += time.time() - start

        return result
    return wrapper

# Only accessed by the solid solver

def only_solid(func: object):
    def wrapper(*args: tuple, **kwargs: dict):

        if CW.rank == 1: result = func(*args, **kwargs)
        else: result = None

        return result
    return wrapper

# Only accessed when mechanical coupling

def only_mechanical(func: object):
    def wrapper(*args: tuple, **kwargs: dict):

        global ResMech
        if ResMech: result = func(*args, **kwargs)
        else: result = None

        return result
    return wrapper

# Only accessed when thermal coupling

def only_thermal(func: object):
    def wrapper(*args: tuple, **kwargs: dict):

        global ResTher
        if ResTher: result = func(*args, **kwargs)
        else: result = None

        return result
    return wrapper

# |------------------------------------|
# |   Initialize the Global Classes    |
# |------------------------------------|

def set_step(dt: float, dt_save: float):

    from . import manager

    global Step
    Step = manager.TimeStep(dt, dt_save)
    return Step

def set_algorithm(algorithm: object, *arg: tuple):

    global Algo
    Algo = algorithm(*arg)
    return Algo

def set_interpolator(interpolator: object, *arg: tuple):

    global Interp
    Interp = interpolator(*arg)
    return Interp

def set_mechanical_res(tol: float):

    from . import manager

    global ResMech
    ResMech = manager.Residual(tol)
    return ResMech

def set_thermal_res(tol: float):

    from . import manager

    global ResTher
    ResTher = manager.Residual(tol)
    return ResTher

def simulate(end_time: float):

    global Algo
    return Algo.simulate(end_time)

# |----------------------------------------|
# |   Import and Initialize the Solvers    |
# |----------------------------------------|

@write_logs
def set_solver(path_F: str, path_S: str):

    global Solver

    if CW.rank == 0:

        from ..solver.pfem_3D import PFEM3D
        Solver = PFEM3D(path_F)

    elif CW.rank == 1:

        from ..solver.metafor import Metafor
        Solver = Metafor(path_S)

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
