from ..general import toolbox as tb
from .block_gauss import BGS
import numpy as np

# Interface quasi-Newton with multi-vector Jacobian class

class MVJ(BGS):
    def __init__(self, max_iter: int):
        '''
        Initialize the interface quasi-Newton with multi-vector Jacobian class
        '''

        BGS.__init__(self, max_iter)

        # Initialize the quantities stored from previous iterations

        object.__setattr__(self, 'prev_disp', np.ndarray(0))
        object.__setattr__(self, 'prev_temp', np.ndarray(0))

        # Store the displacement differences between iterations

        object.__setattr__(self, 'V_disp', list())
        object.__setattr__(self, 'W_disp', list())

        # Current and previous Jacobians for mechanical coupling

        object.__setattr__(self, 'J_disp', np.ndarray(0))
        object.__setattr__(self, 'prev_J_disp', np.ndarray(0))

        # Store the temperature differences between iterations

        object.__setattr__(self, 'V_temp', list())
        object.__setattr__(self, 'W_temp', list())

        # Current and previous Jacobians for thermal coupling

        object.__setattr__(self, 'J_temp', np.ndarray(0))
        object.__setattr__(self, 'prev_J_temp', np.ndarray(0))

    @tb.only_mechanical
    def update_displacement(self):
        '''
        Update the predicted displacement with the predictor increment
        '''

        disp = tb.Solver.get_position()

        # Flatten the residual displacement along a single line

        R = np.hstack(-tb.Res.residual_disp)

        # Remove the previous Jaobian if the last time step failed

        if not self.verified:
            #self.prev_J_disp = np.ndarray(0) # !!!!
            pass

        # Store the previous Jacobian if the last time step converged

        elif not self.iteration:
            self.prev_J_disp = np.copy(self.J_disp)

        # Clear the history matrices from the previous time step

        if not self.iteration:

            self.V_disp.clear()
            self.W_disp.clear()

        # If the current iteration is not the first

        else:

            # Compute and flatten the residual and displacement deltas

            W = np.hstack(disp-self.prev_disp)
            V = np.hstack(tb.Res.residual_disp-tb.Res.prev_res_disp)

            # Add those new deltas at the begining of the history

            self.W_disp.insert(0, W)
            self.V_disp.insert(0, V)

        # Check if no history matrices are available

        if not len(self.V_disp):

            # Perform a BGS iteration if no previous Jacobian

            if not len(self.prev_J_disp):
                delta = self.omega*tb.Res.residual_disp

            # Use the previous Jacobian for computing the prediction

            else: delta = self.prev_J_disp.dot(R)-R

        # Perform a ILS iteration if no previous Jacobian
        
        elif not len(self.prev_J_disp):

            result = np.linalg.lstsq(self.V_disp, self.W_disp, -1)

            # Compute the current Jacobian and the predictor increment

            self.J_disp = np.transpose(result[0])
            delta = self.J_disp.dot(R)-R

        # Perform a MVJ iteration if a previous Jacobian is available

        else:

            X = self.W_disp-np.dot(self.V_disp, self.prev_J_disp.T)
            result = np.linalg.lstsq(self.V_disp, X, -1)

            # Compute the current Jacobian and the predictor increment

            self.J_disp = self.prev_J_disp+np.transpose(result[0])
            delta = self.J_disp.dot(R)-R

        # Actually update the pedicted interface displacement

        tb.Interp.disp += delta.reshape(tb.Res.residual_disp.shape)
        self.prev_disp = np.copy(disp)

    @tb.only_thermal
    def update_temperature(self):
        '''
        Update the predicted temperature with the predictor increment
        '''

        temp = tb.Solver.get_temperature()

        # Flatten the residual displacement along a single line

        R = np.hstack(-tb.Res.residual_temp)

        # Remove the previous Jaobian if the last time step failed

        if not self.verified:
            # self.prev_J_temp = np.ndarray(0) # !!!!
            pass

        # Store the previous Jacobian if the last time step converged

        elif not self.iteration:
            self.prev_J_temp = np.copy(self.J_temp)

        # Clear the history matrices from the previous time step

        if not self.iteration:

            self.V_temp.clear()
            self.W_temp.clear()

        # If the current iteration is not the first

        else:

            # Compute and flatten the residual and temperature deltas

            W = np.hstack(temp-self.prev_temp)
            V = np.hstack(tb.Res.residual_temp-tb.Res.prev_res_temp)

            # Add those new deltas at the begining of the history

            self.W_temp.insert(0, W)
            self.V_temp.insert(0, V)

        # Check if no history matrices are available

        if not len(self.V_temp):

            # Perform a BGS iteration if no previous Jacobian

            if not len(self.prev_J_temp):
                delta = self.omega*tb.Res.residual_temp

            # Use the previous Jacobian for computing the prediction

            else: delta = self.prev_J_temp.dot(R)-R

        # Perform a ILS iteration if no previous Jacobian
        
        elif not len(self.prev_J_temp):

            result = np.linalg.lstsq(self.V_temp, self.W_temp, -1)

            # Compute the current Jacobian and the predictor increment

            self.J_temp = np.transpose(result[0])
            delta = self.J_temp.dot(R)-R

        # Perform a MVJ iteration if a previous Jacobian is available

        else:

            X = self.W_temp-np.dot(self.V_temp, self.prev_J_temp.T)
            result = np.linalg.lstsq(self.V_temp, X, -1)

            # Compute the current Jacobian and the predictor increment

            self.J_temp = self.prev_J_temp+np.transpose(result[0])
            delta = self.J_temp.dot(R)-R

        # Actually update the pedicted interface temperature

        tb.Interp.temp += delta.reshape(tb.Res.residual_temp.shape)
        self.prev_temp = np.copy(temp)
