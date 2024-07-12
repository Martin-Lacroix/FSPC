from ..general import toolbox as tb
from .block_gauss import BGS
import numpy as np

# Inverse least squares approximate Jacobian class

class InvJacobian(object):
    def __init__(self):
        '''
        Initialize the approximate inverse Jacobian class
        '''

        # Store the residual differences between iterations

        object.__setattr__(self, 'V', list())

        # Store the displacement differences between iterations

        object.__setattr__(self, 'W', list())

    def delta(self, residual: np.ndarray):
        '''
        Compute the predictor increment using the current Jacobian
        '''

        # Transform V and W into appropriate numpy matrices

        V = np.flip(np.transpose(self.V), axis=1)
        W = np.flip(np.transpose(self.W), axis=1)

        # Flatten the residual dimensions and take the opposite

        R = np.hstack(-residual)

        # Return the increment for the interface predictor

        delta = np.dot(W, np.linalg.lstsq(V, R, -1)[0])-R
        return np.split(delta, tb.Solver.get_size())

# Interface quasi-Newton with inverse least squares class

class ILS(BGS):
    def __init__(self, max_iter: int):
        '''
        Initialize the interface quasi-Newton with inverse least squares class
        '''

        BGS.__init__(self, max_iter)

        # Initialise the classes of inverse Jacobians

        object.__setattr__(self, 'jac_mecha', InvJacobian())
        object.__setattr__(self, 'jac_therm', InvJacobian())

        # Initialize the quantities stored from previous iterations

        object.__setattr__(self, 'prev_disp', np.ndarray(0))
        object.__setattr__(self, 'prev_temp', np.ndarray(0))

    @tb.only_mechanical
    def update_displacement(self):
        '''
        Update the predicted displacement with the predictor increment
        '''

        disp = tb.Solver.get_position()

        # Perform a BGS iteration if no previous residual is available

        if self.iteration == 0:

            # Remove the deltas stored at the previous time step

            self.jac_mecha.V.clear()
            self.jac_mecha.W.clear()

            # Use the default omega since we cannot use Aitken

            delta = self.omega*tb.ResMech.residual

        # Perform a IQN iteration using the residual history

        else:

            # Flatten the position and residual differences

            W = np.hstack(disp-self.prev_disp)
            V = np.hstack(tb.ResMech.residual-tb.ResMech.prev_res)

            # Add the new deltas at the end of the history list

            self.jac_mecha.W.append(W)
            self.jac_mecha.V.append(V)

            # Compute the interface displacement predictor increment

            delta = self.jac_mecha.delta(tb.ResMech.residual)

        # Update the pedicted interface displacement

        tb.Interp.disp += delta
        self.prev_disp = np.copy(disp)

    @tb.only_thermal
    def update_temperature(self):
        '''
        Update the predicted temperature with the predictor increment
        '''

        temp = tb.Solver.get_temperature()

        # Perform a BGS iteration if no previous residual is available

        if self.iteration == 0:

            # Remove the deltas stored at the previous time step

            self.jac_mecha.V.clear()
            self.jac_mecha.W.clear()

            # Use the default omega since we cannot use Aitken

            delta = self.omega*tb.ResTher.residual

        # Perform a IQN iteration using the residual history

        else:

            # Flatten the temperature and residual differences

            W = np.hstack(temp-self.prev_temp)
            V = np.hstack(tb.ResTher.residual-tb.ResTher.prev_res)

            # Add the new deltas at the end of the history list

            self.jac_therm.W.append(W)
            self.jac_therm.V.append(V)

            # Compute the interface temperature predictor increment

            delta = self.jac_therm.delta(tb.ResTher.residual)

        # Update the pedicted interface temperature

        tb.Interp.temp += delta
        self.prev_temp = np.copy(temp)
