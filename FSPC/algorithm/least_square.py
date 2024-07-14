from ..general import toolbox as tb
from .block_gauss import BGS
import numpy as np

# Interface quasi-Newton with inverse least squares class

class ILS(BGS):
    def __init__(self, max_iter: int):
        '''
        Initialize the interface quasi-Newton with inverse least squares class
        '''

        BGS.__init__(self, max_iter)

        # Initialize the quantities stored from previous iterations

        object.__setattr__(self, 'prev_disp', np.ndarray(0))
        object.__setattr__(self, 'prev_temp', np.ndarray(0))

        # Store the displacement differences between iterations

        object.__setattr__(self, 'V_disp', list())
        object.__setattr__(self, 'W_disp', list())

        # Store the temperature differences between iterations

        object.__setattr__(self, 'V_temp', list())
        object.__setattr__(self, 'W_temp', list())

    @tb.only_mechanical
    def update_displacement(self):
        '''
        Update the predicted displacement with the predictor increment
        '''

        disp = tb.Solver.get_position()

        # Perform a BGS iteration if no previous residual is available

        if self.iteration == 0:

            # Clear the history matrices from the previous time step

            self.V_disp.clear()
            self.W_disp.clear()

            # Use the default omega since we cannot use Aitken

            delta = self.omega*tb.Res.residual_disp

        # Perform a IQN iteration using the residual history

        else:

            # Compute and flatten the residual and displacement deltas

            W = np.hstack(disp-self.prev_disp)
            V = np.hstack(tb.Res.residual_disp-tb.Res.prev_res_disp)

            # Add those new deltas at the begining of the history

            self.W_disp.insert(0, W)
            self.V_disp.insert(0, V)

            # Transpose and transform V and W into numpy matrices

            V = np.transpose(self.V_disp)
            W = np.transpose(self.W_disp)

            # Compute the increment for the interface predictor

            R = np.hstack(-tb.Res.residual_disp)
            delta = np.dot(W, np.linalg.lstsq(V, R, -1)[0])-R

        # Actually update the pedicted interface displacement

        tb.Interp.disp += delta.reshape(tb.Res.residual_disp.shape)
        self.prev_disp = np.copy(disp)

    @tb.only_thermal
    def update_temperature(self):
        '''
        Update the predicted temperature with the predictor increment
        '''

        temp = tb.Solver.get_temperature()

        # Perform a BGS iteration if no previous residual is available

        if self.iteration == 0:

            # Clear the history matrices from the previous time step

            self.V_temp.clear()
            self.W_temp.clear()

            # Use the default omega since we cannot use Aitken

            delta = self.omega*tb.Res.residual_temp

        # Perform a IQN iteration using the residual history

        else:

            # Compute and flatten the residual and temperature deltas

            W = np.hstack(temp-self.prev_temp)
            V = np.hstack(tb.Res.residual_temp-tb.Res.prev_res_temp)

            # Add those new deltas at the begining of the history

            self.W_temp.insert(0, W)
            self.V_temp.insert(0, V)

            # Transpose and transform V and W into numpy matrices

            V = np.transpose(self.V_temp)
            W = np.transpose(self.W_temp)

            # Compute the increment for the interface predictor

            R = np.hstack(-tb.Res.residual_temp)
            delta = np.dot(W, np.linalg.lstsq(V, R, -1)[0])-R

        # Actually update the pedicted interface temperature

        tb.Interp.temp += delta.reshape(tb.Res.residual_temp.shape)
        self.prev_temp = np.copy(temp)
