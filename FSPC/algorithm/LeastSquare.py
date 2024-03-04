from mpi4py.MPI import COMM_WORLD as CW
from ..general import Toolbox as tb
from .Algorithm import Algorithm
import numpy as np

# |--------------------------------------------------|
# |   Interface Quasi-Newton Inverse Least Square    |
# |--------------------------------------------------|

class ILS(Algorithm):
    def __init__(self,maxIter):

        Algorithm.__init__(self)
        self.maxIter = maxIter
        self.omega = 0.5

# |---------------------------------|
# |   Coupling at Each Time Step    |
# |---------------------------------|

    def couplingAlgo(self):

        self.iteration = 0
        while self.iteration < self.maxIter:

            # Transfer and fluid solver call

            self.transferDirichlet()
            if not self.runFluid(): return False

            # Transfer and solid solver call

            self.transferNeumann()
            if not self.runSolid(): return False

            # Compute the coupling residual

            output = self.relaxation()
            verified = CW.bcast(output,root=1)

            # Exit the loop if the solution is converged

            self.iteration += 1
            if verified: return True
            else: self.wayBack()
        
        return False

# |--------------------------------------|
# |   Compute the Solution Correction    |
# |--------------------------------------|

    def __compute(self,conv):
        
        V = np.flip(np.transpose(conv.V),axis=1)
        W = np.flip(np.transpose(conv.W),axis=1)
        R = np.hstack(-conv.residual)

        # Return the solution correction

        delta = np.dot(W,np.linalg.lstsq(V,R,-1)[0])-R
        return np.split(delta,tb.Solver.getSize())

# |-------------------------------------------------|
# |   Relaxation of Solid Interface Displacement    |
# |-------------------------------------------------|
    
    @tb.conv_mecha
    def updateDisplacement(self):

        disp = tb.Solver.getPosition()

        # Perform either BGS or IQN iteration

        if self.iteration == 0:

            tb.ResMech.V = list()
            tb.ResMech.W = list()
            delta = self.omega*tb.ResMech.residual

        else:
            tb.ResMech.V.append(np.hstack(tb.ResMech.deltaRes()))
            tb.ResMech.W.append(np.hstack(disp-self.prevDisp))
            delta = self.__compute(tb.ResMech)

        # Update the pedicted displacement

        tb.Interp.disp += delta
        self.prevDisp = np.copy(disp)

# |------------------------------------------------|
# |   Relaxation of Solid Interface Temperature    |
# |------------------------------------------------|

    @tb.conv_therm
    def updateTemperature(self):

        temp = tb.Solver.getTemperature()

        # Perform either BGS or IQN iteration

        if self.iteration == 0:

            tb.ResTher.V = list()
            tb.ResTher.W = list()
            delta = self.omega*tb.ResTher.residual

        else:
            tb.ResTher.V.append(np.hstack(tb.ResTher.deltaRes()))
            tb.ResTher.W.append(np.hstack(temp-self.prevTemp))
            delta = self.__compute(tb.ResTher)

        # Update the predicted temperature

        tb.Interp.temp += delta
        self.prevTemp = np.copy(temp)
