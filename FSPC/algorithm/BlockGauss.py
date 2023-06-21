from mpi4py.MPI import COMM_WORLD as CW
from .Algorithm import Algorithm
from .. import Toolbox as tb
import numpy as np

# %% Block-Gauss Seidel with Aitken Dynamic Relaxation

class BGS(Algorithm):
    def __init__(self):
        
        Algorithm.__init__(self)
        self.omega = 0.5

# %% Coupling at Each Time Step

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

            self.computeResidual()
            self.updateConverg()
            self.relaxation()

            # Check the converence of the FSI

            verif = self.verified()
            verif = CW.scatter([verif,verif],root=1)

            # End of the coupling iteration

            self.iteration += 1
            if verif: return True
        
        return False

# %% Relaxation of Solid Interface Displacement

    @tb.conv_mecha
    def relaxationM(self):

        if self.iteration == 0:
            self.omegaP = self.omega

        else:

            dRes = self.resP-self.prevResP
            alpha = np.tensordot(dRes,dRes)
            alpha /= np.tensordot(dRes,self.prevResP)
            self.omegaP = max(min(-self.omegaP*alpha,1),0)

        # Updates the residuals and displacement

        self.prevResP = np.copy(self.resP)
        tb.interp.pos += self.omegaP*self.resP

# %% Relaxation of Solid Interface Temperature

    @tb.conv_therm
    def relaxationT(self):

        if self.iteration == 0:
            self.omegaT = self.omega

        else:

            dRes = self.resT-self.prevResT
            alpha = np.tensordot(dRes,dRes)
            alpha /= np.tensordot(dRes,self.prevResT)
            self.omegaT = max(min(-self.omegaT*alpha,1),0)

        # Updates the residuals and displacement

        self.prevResT = np.copy(self.resT)
        tb.interp.pos += self.omegaT*self.resT
    