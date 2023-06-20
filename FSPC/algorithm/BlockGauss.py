from mpi4py.MPI import COMM_WORLD as CW
from .Algorithm import Algorithm
from .. import Toolbox as tb
import numpy as np

# %% Block-Gauss Seidel with Aitken Dynamic Relaxation

class BGS(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)

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

    @tb.only_mecha
    def relaxationM(self):

        if self.aitken: correction = self.getOmegaP()*self.resP
        else: correction = self.omega*self.resP
        tb.interp.pos += correction

    # Compute omega with Aitken relaxation

    @tb.only_mecha
    def getOmegaP(self):

        if self.iteration == 0:
            self.omegaP = self.omega

        else:

            dRes = self.resP-self.prevResPos
            prodRes = np.sum(dRes*self.prevResPos)
            dResNormSqr = np.sum(np.linalg.norm(dRes,axis=0)**2)
            if dResNormSqr != 0: self.omegaP *= -prodRes/dResNormSqr
            else: self.omegaP = 0

        # Changes omega if out of the range

        self.omegaP = min(self.omegaP,1)
        self.omegaP = max(self.omegaP,0)
        self.prevResPos = np.copy(self.resP)
        return self.omegaP

# %% Relaxation of Solid Interface Temperature

    @tb.only_therm
    def relaxationT(self):

        if self.aitken: correction = self.getOmegaT()*self.resT
        else: correction = self.omega*self.resT
        tb.interp.temp += correction

    # Compute omega with Aitken relaxation

    @tb.only_therm
    def getOmegaT(self):

        if self.iteration == 0:
            self.omegaT = self.omega

        else:

            dRes = self.resT-self.prevResTemp
            prodRes = np.sum(dRes*self.prevResTemp)
            dResNormSqr = np.sum(np.linalg.norm(dRes,axis=0)**2)
            if dResNormSqr != 0: self.omegaT *= -prodRes/dResNormSqr
            else: self.omegaT = 0

        # Changes omega if out of the range

        self.omegaT = min(self.omegaT,1)
        self.omegaT = max(self.omegaT,0)
        self.prevResTemp = np.copy(self.resT)
        return self.omegaT
    