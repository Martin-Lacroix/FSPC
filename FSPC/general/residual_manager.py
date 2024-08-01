from . import toolbox as tb
import numpy as np

# Coupling convergence and residual manager class

class Residual(tb.Static):
    def __init__(self, tol: float):
        '''
        Initialize the coupling convergence and residual manager class
        '''

        # User-defined tolerance and the residual to compare

        object.__setattr__(self, 'tol', tol)

        # Initial epsilon should be higher than its first estimate

        object.__setattr__(self, 'epsilon_disp', np.inf)
        object.__setattr__(self, 'epsilon_temp', np.inf)

        # Dimensional and per-node version of the displacement residual

        object.__setattr__(self, 'prev_res_disp', np.ndarray(0))
        object.__setattr__(self, 'residual_disp', np.ndarray(0))

        # Dimensional and per-node version of the temperature residual

        object.__setattr__(self, 'prev_res_temp', np.ndarray(0))
        object.__setattr__(self, 'residual_temp', np.ndarray(0))

    def reset(self):
        '''
        Reset the class attributes to their default values
        '''

        # Re-initialize the per-node displacement residuals

        self.prev_res_disp = np.ndarray(0)
        self.residual_disp = np.ndarray(0)

        # Re-initialize the per-node temperature residuals

        self.prev_res_temp = np.ndarray(0)
        self.residual_temp = np.ndarray(0)

        # Re-initialize the scalar convergence indicator

        self.epsilon_disp = np.inf
        self.epsilon_temp = np.inf

    @tb.only_mechanical
    def update_res_mech(self):
        '''
        Compute the residual and update the convergence criterion
        '''

        displacement = tb.Solver.get_position()

        # Update the previous and current displacement residuals

        self.prev_res_disp = np.copy(self.residual_disp)
        self.residual_disp = displacement-tb.Interp.disp

        # Compute the norm of the residual over each dimension

        res = np.linalg.norm(self.residual_disp, axis=0)
        den = np.linalg.norm(displacement, axis=0)

        # Compute the norm of the dimensions then normalize

        res = res/(den+self.tol)
        self.epsilon_disp = np.linalg.norm(res)

    @tb.only_thermal
    def update_res_ther(self):
        '''
        Compute the residual and update the convergence criterion
        '''

        temperature = tb.Solver.get_temperature()

        # Update the previous and current temperature residuals

        self.prev_res_temp = np.copy(self.residual_temp)
        self.residual_temp = temperature-tb.Interp.temp

        # Compute the norm of the residual over each dimension

        res = np.linalg.norm(self.residual_temp, axis=0)
        den = np.linalg.norm(temperature, axis=0)

        # Compute the norm of the dimensions then normalize

        res = res/(den+self.tol)
        self.epsilon_temp = np.linalg.norm(res)

    def check(self):
        '''
        Returns true if the convergence criterion is satisfied
        '''

        # Return false if the mechanical tolerance is not reached

        if tb.has_mecha and (self.epsilon_disp > self.tol):
            return False

        # Return false if the thermal tolerance is not reached

        if tb.has_therm and (self.epsilon_temp > self.tol):
            return False

        # Return true if none of the above check failed

        return True

    def display_residual(self):
        '''
        Print the current state of the convergence criterion
        '''

        if tb.has_mecha:

            # Print the normalized residual for the mechanical coupling

            epsilon = f'Residual Mech : {self.epsilon_disp:.3e}'
            print(f'[{tb.Algo.iteration}]', epsilon)

        if tb.has_therm:

            # Print the normalized residual for the thermal coupling

            epsilon = f'Residual Ther : {self.epsilon_temp:.3e}'
            print(f'[{tb.Algo.iteration}]', epsilon)
