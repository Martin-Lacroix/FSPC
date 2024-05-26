from .general import toolbox

# Import the base FSPC modules

from . import general
from . import algorithm
from . import interpolator

# Convert std::cout to Python print

try:
    import python_stream
    redirect = python_stream.Redirect()
except: redirect = None

# |---------------------------------------|
# |   Define the Initializer Functions    |
# |---------------------------------------|

def set_time_step(step_manager: general.TimeStep):
    
    toolbox.__setattr__('Step', step_manager)

def set_algorithm(algorithm: algorithm.Algorithm):

    toolbox.__setattr__('Algo', algorithm)

def set_interpolator(interpolator: interpolator.Interpolator):

    toolbox.__setattr__('Interp', interpolator)

def set_mechanical_res(residual: general.Residual):

    toolbox.has_mecha = True
    toolbox.__setattr__('ResMech', residual)

def set_thermal_res(residual: general.Residual):

    toolbox.has_therm = True
    toolbox.__setattr__('ResTher', residual)

# |-------------------------------------|
# |   Initialize the Solver Wrappers    |
# |-------------------------------------|

@toolbox.write_logs
def init_solver(path_F: str, path_S: str):

    if toolbox.is_fluid():

        from .solver.pfem_3D import PFEM3D
        toolbox.__setattr__('Solver', PFEM3D(path_F))

    if toolbox.is_solid():

        from .solver.metafor import Metafor
        toolbox.__setattr__('Solver', Metafor(path_S))

    return toolbox.Solver
