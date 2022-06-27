from .algorithm import Algorithm
from ..tools import printY,scatterFS,scatterSF
import numpy as np

# %% Block-Gauss Seidel with Aitken Dynamic Relaxation

class BGS_ADR(Algorithm):
    def __init__(self,input,param,com):
        Algorithm.__init__(self,input,param,com)

        self.omegaMin = 1e-12
        self.omega = param['omega']
        self.aitken = param['aitken']
        self.omegaMax = param['omega']

# %% Coupling at Each Time Step

    def couplingAlgo(self,com):

        verified = False
        self.iteration = 0
        if com.rank == 1: self.converg.epsilon = np.inf

        while True:
            print('FSI iteration {}'.format(self.iteration))

            # Solid to fluid mechanical transfer

            self.clock['Communication'].start()
            self.transferDispSF(com)
            self.clock['Communication'].end()

            # Fluid solver call for FSI subiteration

            printY('Launching fluid solver\n')

            if com.rank == 0:

                self.clock['Solver run'].start()
                verified = self.solver.run(*self.step.timeFrame())
                self.clock['Solver run'].end()

            verified = scatterFS(verified,com)
            if not verified: return False
                
            # Fluid to solid mechanical transfer

            self.clock['Communication'].start()
            self.transferLoadFS(com)
            self.clock['Communication'].end()

            # Solid solver call for FSI subiteration
            
            printY('Launching solid solver\n')

            if com.rank == 1:

                self.clock['Solver run'].start()
                verified = self.solver.run(*self.step.timeFrame())
                self.clock['Solver run'].end()

            verified = scatterSF(verified,com)
            if not verified: return False

            # Compute the mechanical residual

            if com.rank == 1:
            
                self.residualDispS()
                self.converg.update(self.residual)
                self.logIter.write(self.iteration,self.converg.epsilon)
                print('Residual =',self.converg.epsilon)

                # Use BGS relaxation for solid displacement
            
                self.clock['Relax BGS-ADR'].start()
                self.relaxation()
                self.clock['Relax BGS-ADR'].end()

            # Check the converence of the FSI

            if com.rank == 1: verified = self.converg.isVerified()
            verified = scatterSF(verified,com)

            # End of the coupling iteration

            if verified: break
            self.iteration += 1
            if self.iteration > self.iterMax: return False
        
        return True

# %% BGS Relaxation of Solid Displacement

    def relaxation(self):

        if self.aitken: self.setOmega()
        self.interp.disp += self.omega*self.residual

    # Compute omega with Aitken relaxation

    def setOmega(self):

        if self.iteration == 0:
            self.omega = max(self.omegaMax,self.omega)

        else:

            dRes = self.residual-self.prevResidual
            prodRes = np.sum(dRes*self.prevResidual)
            dResNormSqr = np.sum(np.linalg.norm(dRes,axis=0)**2)
            if dResNormSqr != 0: self.omega *= -prodRes/dResNormSqr
            else: self.omega = self.omegaMin

        # Changes omega if out of the range

        self.omega = min(self.omega,1)
        self.omega = max(self.omega,self.omegaMin)
        self.prevResidual = self.residual.copy()