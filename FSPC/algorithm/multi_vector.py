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

        # Current Jacobian and Jacobian at previous time step

        object.__setattr__(self, 'J', np.ndarray(0))
        object.__setattr__(self, 'prev_J', np.ndarray(0))

    def update(self):
        '''
        Copy the current Jacobian into the previous Jacobian
        '''

        # Explicit numpy copy to prevent variable dependency

        self.prev_J = np.copy(self.J)

    def set_zero(self, size: int):
        '''
        Reset the class attributes to their default values
        '''

        # The size of the Jacobian is the number of FSI nodes × DDL

        self.J = np.zeros((size, size))
        self.prev_J = np.zeros((size, size))

    def delta(self, residual: np.ndarray):
        '''
        Compute the predictor increment using the previous Jacobian
        '''

        # Transform V and W into appropriate numpy matrices

        V = np.flip(np.transpose(self.V), axis=1)
        W = np.flip(np.transpose(self.W), axis=1)

        # Flatten the residual dimensions and take the opposite

        R = np.hstack(-residual)

        # Compute the inverse Jacobian increment

        X = np.transpose(W-np.dot(self.prev_J, V))
        correction = np.transpose(np.linalg.lstsq(V.T, X, -1)[0])

        # Compute the current inverse Jacobian from the previous one

        self.J = self.prev_J+correction

        # Return the increment for the interface predictor

        delta = np.dot(self.J, R)-R
        return np.split(delta, tb.Solver.get_size())

# Interface quasi-Newton with multi-vector Jacobian class

class MVJ(BGS):
    def __init__(self, max_iter: int):
        '''
        Initialize the interface quasi-Newton with multi-vector Jacobian class
        '''

        BGS.__init__(self, max_iter)

        # Initialise the classes of inverse Jacobians

        object.__setattr__(self, 'jac_mecha', InvJacobian())
        object.__setattr__(self, 'jac_therm', InvJacobian())

        # Initialize the quantities stored from previous iterations

        object.__setattr__(self, 'prev_disp', np.ndarray(0))
        object.__setattr__(self, 'prev_temp', np.ndarray(0))
    
    @tb.only_solid
    def update(self, verified: bool):
        '''
        Copy the current Jacobian into the previous Jacobian
        '''

        if not verified: return
        if tb.has_mecha: self.jac_mecha.update()
        if tb.has_therm: self.jac_therm.update()

    @tb.only_mechanical
    def update_displacement(self):
        '''
        Update the predicted displacement with the predictor increment
        '''

        disp = tb.Solver.get_position()

        # If no previous iterations are available

        if self.iteration == 0:

            # Remove the deltas stored at the previous time step

            self.jac_mecha.V.clear()
            self.jac_mecha.W.clear()

            # Perform a BGS iteration if the previous coupling failed

            if not self.verified:

                # Use the default omega since we cannot use Aitken

                self.jac_mecha.set_zero(tb.ResMech.residual.size)
                delta = self.omega*tb.ResMech.residual

            # Use the Jacobian from the previous time step

            else:

                R = np.hstack(-tb.ResMech.residual)

                # Compute the interface displacement predictor increment

                delta = np.dot(self.jac_mecha.prev_J, R)-R
                delta = np.split(delta, tb.Solver.get_size())

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

        # If no previous iterations are available

        if self.iteration == 0:

            # Remove the deltas stored at the previous time step

            self.jac_therm.V.clear()
            self.jac_therm.W.clear()
            
            # Perform a BGS iteration if the previous coupling failed

            if not self.verified:

                # Use the default omega since we cannot use Aitken

                self.jac_therm.set_zero(tb.ResTher.residual.size)
                delta = self.omega*tb.ResTher.residual

            # Use the Jacobian from the previous time step

            else:

                R = np.hstack(-tb.ResTher.residual)

                # Compute the interface temperature predictor increment

                delta = np.dot(self.jac_therm.prev_J, R)-R
                delta = np.split(delta, tb.Solver.get_size())

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
