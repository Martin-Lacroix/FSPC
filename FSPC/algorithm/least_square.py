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

        # Transform V and W into numpy matrices

        V = np.transpose(self.V)
        W = np.transpose(self.W)

        # Compute the increment for the interface predictor

        R = np.hstack(-residual)
        delta = np.dot(W, np.linalg.lstsq(V, R, -1)[0])-R

        # Reshape such that each dimension is along a column

        return delta.reshape(residual.shape)

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

            delta = self.omega*tb.Res.residual_disp

        # Perform a IQN iteration using the residual history

        else:

            # Flatten the displacement and residual differences

            W = np.hstack(disp-self.prev_disp)
            V = np.hstack(tb.Res.residual_disp-tb.Res.prev_res_disp)

            # Add the new deltas at the end of the history list

            self.jac_mecha.W.insert(0, W)
            self.jac_mecha.V.insert(0, V)

            # Compute the interface displacement predictor increment

            delta = self.jac_mecha.delta(tb.Res.residual_disp)

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

            self.jac_therm.V.clear()
            self.jac_therm.W.clear()

            # Use the default omega since we cannot use Aitken

            delta = self.omega*tb.Res.residual_temp

        # Perform a IQN iteration using the residual history

        else:

            # Flatten the temperature and residual differences

            W = np.hstack(temp-self.prev_temp)
            V = np.hstack(tb.Res.residual_temp-tb.Res.prev_res_temp)

            # Add the new deltas at the end of the history list

            self.jac_therm.W.insert(0, W)
            self.jac_therm.V.insert(0, V)

            # Compute the interface temperature predictor increment

            delta = self.jac_therm.delta(tb.Res.residual_temp)

        # Update the pedicted interface temperature

        tb.Interp.temp += delta
        self.prev_temp = np.copy(temp)
