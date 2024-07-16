from contextlib import redirect_stdout as stdout
from contextlib import redirect_stderr as stderr
from mpi4py.MPI import COMM_WORLD as CW
from typing import Callable
import time

# Global variables for fluid-structure coupling

has_mecha = False
has_therm = False

# Check if we are on the solid of the fluid processes

def is_fluid(): return CW.rank == 0
def is_solid(): return CW.rank == 1

# The clock will store the measured computation times

import collections
clock = collections.defaultdict(float)

# Static class that prevents dynamic attribute creation

class Static(object):

    def __setattr__(self, key: str, value):

        # Raise an exception of the attrubite does not exist
        
        if not hasattr(self, key): raise Exception('Unknown attribute '+key)

        # Update the attribute if it already exists in the class

        else: object.__setattr__(self, key, value)

def write_logs(function: Callable):
    '''
    Decorator that copy the print calls into a file
    '''

    def wrapper(*args):

        rank = str(CW.rank)

        # Open the file solver_rank.txt or create if not exist

        with open('solver_'+rank+'.txt', 'a') as output:

            # This will capture both stdout and stderr from Python

            with stderr(output), stdout(output):
                return function(*args)

    return wrapper

def compute_time(function: Callable):
    '''
    Decorator that measures the computation time of a function
    '''

    def wrapper(*args):

        # Store the current time then run the decorated function

        start = time.time()
        result = function(*args)

        # Build the name of the function to use in the clock

        parent = args[0].__class__.__name__+' : '
        clock[parent+function.__name__] += time.time()-start

        # Return the result of the timed function if any

        return result
    return wrapper

def only_solid(function: Callable):
    '''
    Decorator that restricts the function call to the solid rank
    '''

    def wrapper(*args):

        # Run the function only if we are on the solid process

        if is_solid(): return function(*args)

    return wrapper

def only_mechanical(function: Callable):
    '''
    Decorator that restricts the function call to mechanical coupling
    '''

    def wrapper(*args):

        # Run the function only if mechanical coupling is enabled

        if has_mecha: return function(*args)

    return wrapper

def only_thermal(function: Callable):
    '''
    Decorator that restricts the function call to thermal coupling
    '''

    def wrapper(*args):

        # Run the function only if thermal coupling is enabled

        if has_therm: return function(*args)

    return wrapper

def run_fluid():
    '''
    Run the fluid solver within the current time step
    '''

    # We must use the Solver class outside of the function scope

    global Solver
    verified = False

    # Run the solver only if we are on the fluid process

    if is_fluid():

        verified = Solver.run()
        if not verified: print('Failed to solve PFEM3D')

    # Share the output of the fluid solver with the solid rank

    return CW.bcast(verified, root=0)

def run_solid():
    '''
    Run the solid solver within the current time step
    '''

    # We must use the Solver class outside of the function scope

    global Solver
    verified = False

    # Run the solver only if we are on the solid process

    if is_solid():

        verified = Solver.run()
        if not verified: print('Failed to solve Metafor')

    # Share the output of the solid solver with the fluid rank

    return CW.bcast(verified, root=1)

def print_clock():
    '''
    Print the computation times measured during the simulation
    '''

    # Print the name of the process that is being displayed

    print('\n------------------------------------')
    print('Process {:.0f} : Time Stats'.format(CW.rank))
    print('------------------------------------\n')

    # Loop on all function names that have been stored in clock

    for key, value in clock.items():
        print('{}{:.5f}'.format(key.ljust(25), value))
