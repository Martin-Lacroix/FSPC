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

# |----------------------------------------------|
# |   Print the Computation Time of Functions    |
# |----------------------------------------------|

def print_clock():

    print('\n------------------------------------')
    print('Process {:.0f} : Time Stats'.format(CW.rank))
    print('------------------------------------\n')

    for key, value in clock.items():
        print('{}{:.5f}'.format(key.ljust(25), value))
