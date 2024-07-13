from .general import toolbox

# Import the base fluid-structure modules

from . import general
from . import algorithm
from . import interpolator

# Convert C++ std::cout and std::cerr to Python print

try:
    import python_stream
    redirect = python_stream.Redirect()
except: redirect = None

# Set the global time step class from the user input

def set_time_step(step_manager: general.TimeStep):
    '''
    Initialize the disk exporter and time step manager class
    '''
    
    toolbox.__setattr__('Step', step_manager)

# Set the global algorithm class from the user input

def set_algorithm(algorithm: algorithm.Algorithm):
    '''
    Initialize the fluid-structure coupling algorithm class
    '''

    toolbox.__setattr__('Algo', algorithm)

# Set the global interpolator class from the user input

def set_interpolator(interpolator: interpolator.Interpolator):
    '''
    Initialize the fluid-structure interpolation class
    '''

    toolbox.__setattr__('Interp', interpolator)

# Set the global mechanical residual class from the user input

def set_mechanical_res(residual: general.Residual):
    '''
    Initialize the mechanical convergence and residual manager
    '''

    toolbox.has_mecha = True
    toolbox.__setattr__('Res', residual)

# Set the global thermal residual class from the user input

def set_thermal_res(residual: general.Residual):
    '''
    Initialize the thermal convergence and residual manager
    '''

    toolbox.has_therm = True
    toolbox.__setattr__('Res', residual)

# Set the thermo-mechanical residual class from the user input

def set_thermo_mech_res(residual: general.Residual):
    '''
    Initialize the thermal convergence and residual manager
    '''

    toolbox.has_mecha = True
    toolbox.has_therm = True
    toolbox.__setattr__('Res', residual)

# Set the global solver class from the user input path

@toolbox.write_logs
def init_solver(path_F: str, path_S: str):
    '''
    Initialize the fluid and solid solver wrapper classes
    '''

    if toolbox.is_fluid():

        # Load PFEM3D wrapper if we are on the fluid process

        from .solver.pfem_3D import Solver
        toolbox.__setattr__('Solver', Solver(path_F))

    if toolbox.is_solid():

        # Load Metafor wrapper if we are on the solid process

        from .solver.metafor import Solver
        toolbox.__setattr__('Solver', Solver(path_S))

    # Also return the FSPC object associated to the solver

    return toolbox.Solver
