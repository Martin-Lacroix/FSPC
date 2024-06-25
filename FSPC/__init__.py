from .general import toolbox

# Import the base fluid-structure modules

from . import general
from . import algorithm
from . import interpolator

# Convert C++ std::cout to Python print

try:
    import python_stream
    redirect = python_stream.Redirect()
except: redirect = None

# Initialize the fluid-structure coupling classes

def set_time_step(step_manager: general.TimeStep):
    '''
    Initialize the disk exporter and time step manager class
    '''
    
    toolbox.__setattr__('Step', step_manager)

def set_algorithm(algorithm: algorithm.Algorithm):
    '''
    Initialize the fluid-structure coupling algorithm class
    '''

    toolbox.__setattr__('Algo', algorithm)

def set_interpolator(interpolator: interpolator.Interpolator):
    '''
    Initialize the fluid-structure interpolation class
    '''

    toolbox.__setattr__('Interp', interpolator)

def set_mechanical_res(residual: general.Residual):
    '''
    Initialize the mechanical convergence and residual manager
    '''

    toolbox.has_mecha = True
    toolbox.__setattr__('ResMech', residual)

def set_thermal_res(residual: general.Residual):
    '''
    Initialize the thermal convergence and residual manager
    '''

    toolbox.has_therm = True
    toolbox.__setattr__('ResTher', residual)

@toolbox.write_logs
def init_solver(path_F: str, path_S: str):
    '''
    Initialize the fluid and solid solver wrapper classes
    '''

    if toolbox.is_fluid():

        from .solver.pfem_3D import Solver
        toolbox.__setattr__('Solver', Solver(path_F))

    if toolbox.is_solid():

        from .solver.metafor import Solver
        toolbox.__setattr__('Solver', Solver(path_S))

    return toolbox.Solver
