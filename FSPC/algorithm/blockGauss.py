from ..toolbox import compute_time
from .algorithm import Algorithm
import numpy as np

# %% Block-Gauss Seidel with Aitken Dynamic Relaxation

class BGS_ADR(Algorithm):
    def __init__(self,solver):
        Algorithm.__init__(self,solver)

# %% Coupling at Each Time Step

    def couplingAlgo(self,com):

        verif = False
        self.iteration = 0
        self.converg.epsilon = np.inf
        timeFrame = self.step.timeFrame()

        while True:

            # Transfer and fluid solver call

            self.transferDispSF(com)
            if com.rank == 0: verif = self.solver.run(*timeFrame)
            verif = com.scatter([verif,verif],root=0)
            if not verif: return False
                
            # Transfer and solid solver call

            self.transferLoadFS(com)
            if com.rank == 1: verif = self.solver.run(*timeFrame)
            verif = com.scatter([verif,verif],root=1)
            if not verif: return False

            # Compute the mechanical residual

            if com.rank == 1:
            
                self.residualDispS()
                self.converg.update(self.residual)
                self.printRes()
                self.relaxation()

            # Check the converence of the FSI

            if com.rank == 1: verif = self.converg.isVerified()
            verif = com.scatter([verif,verif],root=1)

            # End of the coupling iteration

            if verif: break
            self.iteration += 1
            if self.iteration > self.iterMax: return False
        
        return True

# %% BGS Relaxation of Solid Displacement

    @compute_time
    def relaxation(self):

        if self.aitken: self.setOmega()
        self.interp.disp += self.omega*self.residual

    # Compute omega with Aitken relaxation

    def setOmega(self):

        if self.iteration == 0:
            self.omega = 0.5

        else:

            dRes = self.residual-self.prevResidual
            prodRes = np.sum(dRes*self.prevResidual)
            dResNormSqr = np.sum(np.linalg.norm(dRes,axis=0)**2)
            if dResNormSqr != 0: self.omega *= -prodRes/dResNormSqr
            else: self.omega = 0

        # Changes omega if out of the range

        self.omega = min(self.omega,1)
        self.omega = max(self.omega,0)
        self.prevResidual = self.residual.copy()