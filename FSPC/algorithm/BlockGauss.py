from mpi4py.MPI import COMM_WORLD as CW
from ..general import Toolbox as tb
from .Algorithm import Algorithm
import numpy as np

# -----------------------------------------------|
# Block-Gauss Seidel Aitken Dynamic Relaxation   |
# -----------------------------------------------|

class BGS(Algorithm):
    def __init__(self):
        
        Algorithm.__init__(self)
        self.omega = 0.5

# -----------------------------|
# Coupling at Each Time Step   |
# -----------------------------|

    def couplingAlgo(self):

        verif = False
        self.iteration = 0
        self.resetConverg()

        while self.iteration < self.maxIter:

            # Transfer and fluid solver call

            self.transferDirichletSF()
            if CW.rank == 0: verif = tb.solver.run()
            verif = CW.scatter([verif,verif],root=0)
            if not verif: return False

            # Transfer and solid solver call

            self.transferNeumannFS()
            if CW.rank == 1: verif = tb.solver.run()
            verif = CW.scatter([verif,verif],root=1)
            if not verif: return False

            # Compute the coupling residual

            verif = self.relaxation()
            verif = CW.scatter([verif,verif],root=1)

            # End of the coupling iteration

            self.iteration += 1
            if verif: return True
        
        return False

# ----------------------------------|
# Compute the Solution Correction   |
# ----------------------------------|

    def compute(self,conv):

        D = conv.deltaRes()
        A = np.tensordot(D,conv.prevRes)

        # Update the Aitken relaxation parameter

        conv.omega = -A*conv.omega/np.tensordot(D,D)
        conv.omega = max(min(conv.omega,1),0)
        return conv.omega*conv.residual

# ---------------------------------------------|
# Relaxation of Solid Interface Displacement   |
# ---------------------------------------------|

    @tb.conv_mecha
    def relaxDisplacement(self):

        if self.iteration > 0:
            tb.interp.disp += self.compute(tb.convMech)

        else:
            tb.convMech.omega = self.omega
            tb.interp.disp += self.omega*tb.convMech.residual

# --------------------------------------------|
# Relaxation of Solid Interface Temperature   |
# --------------------------------------------|

    @tb.conv_therm
    def relaxTemperature(self):

        if self.iteration > 0:
            tb.interp.temp += self.compute(tb.convTher)

        else:
            tb.convTher.omega = self.omega
            tb.interp.temp += self.omega*tb.convTher.residual
    