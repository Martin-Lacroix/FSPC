from contextlib import redirect_stdout as stdout
from contextlib import redirect_stderr as stderr
from mpi4py.MPI import COMM_WORLD as CW
from typing import Callable
import time

# Global variables for fluid-structure coupling

has_mecha = False
has_therm = False

def is_fluid(): return CW.rank == 0
def is_solid(): return CW.rank == 1

import collections
clock = collections.defaultdict(float)

class Static(object):

    def __setattr__(self, key: str, value):
        if not hasattr(self, key): raise Exception('Unknown attribute '+key)
        else: object.__setattr__(self, key, value)

# Definition of the global function decorators

def write_logs(function: Callable):
    '''
    Decorator that copy the print calls into a file
    '''

    def wrapper(*args):

        rank = str(CW.rank)
        with open('solver_'+rank+'.dat', 'a') as output:
            with stderr(output), stdout(output):
                return function(*args)

    return wrapper

def compute_time(function: Callable):
    '''
    Decorator that measures the computation time of a function
    '''

    def wrapper(*args):

        start = time.time()
        result = function(*args)
        parent = args[0].__class__.__name__+' : '
        clock[parent+function.__name__] += time.time()-start

        return result
    return wrapper

def only_solid(function: Callable):
    '''
    Decorator that restricts the function call to the solid rank
    '''

    def wrapper(*args):

        if is_solid(): return function(*args)

    return wrapper

def only_mechanical(function: Callable):
    '''
    Decorator that restricts the function call to mechanical coupling
    '''

    def wrapper(*args):

        if has_mecha: return function(*args)

    return wrapper

def only_thermal(function: Callable):
    '''
    Decorator that restricts the function call to thermal coupling
    '''

    def wrapper(*args):

        if has_therm: return function(*args)

    return wrapper

def run_fluid():
    '''
    Run the fluid solver within the current time step
    '''

    global Solver
    verified = False

    if is_fluid():

        verified = Solver.run()
        if not verified: print('Failed to solve PFEM3D')

    return CW.bcast(verified, root=0)

def run_solid():
    '''
    Run the solid solver within the current time step
    '''

    global Solver
    verified = False

    if is_solid():

        verified = Solver.run()
        if not verified: print('Failed to solve Metafor')

    return CW.bcast(verified, root=1)

def print_clock():
    '''
    Print the computation times measured during the simulation
    '''

    print('\n------------------------------------')
    print('Process {:.0f} : Time Stats'.format(CW.rank))
    print('------------------------------------\n')

    for key, value in clock.items():
        print('{}{:.5f}'.format(key.ljust(25), value))
