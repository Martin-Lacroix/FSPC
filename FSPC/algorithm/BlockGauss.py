from mpi4py.MPI import COMM_WORLD as CW
from ..general import Toolbox as tb
from .Algorithm import Algorithm
import numpy as np

# |---------------------------------------------------|
# |   Block-Gauss Seidel Aitken Dynamic Relaxation    |
# |---------------------------------------------------|

class BGS(Algorithm):
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

        D = conv.deltaRes()
        A = np.tensordot(D,conv.prevRes)

        # Update the Aitken relaxation parameter

        conv.omega = -A*conv.omega/np.tensordot(D,D)
        conv.omega = max(min(conv.omega,1),0)
        return conv.omega*conv.residual

# |-------------------------------------------------|
# |   Relaxation of Solid Interface Displacement    |
# |-------------------------------------------------|

    @tb.conv_mecha
    def updateDisplacement(self):

        if self.iteration > 0:
            tb.Interp.disp += self.__compute(tb.ResMech)

        else:
            tb.ResMech.omega = self.omega
            tb.Interp.disp += self.omega*tb.ResMech.residual

# |------------------------------------------------|
# |   Relaxation of Solid Interface Temperature    |
# |------------------------------------------------|

    @tb.conv_therm
    def updateTemperature(self):

        if self.iteration > 0:
            tb.Interp.temp += self.__compute(tb.ResTher)

        else:
            tb.ResTher.omega = self.omega
            tb.Interp.temp += self.omega*tb.ResTher.residual
    