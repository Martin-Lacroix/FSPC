from .algorithm import Algorithm
from ..tools import printY
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

    def couplingAlgo(self):

        self.iter = 0
        self.converg.epsilon = np.inf

        while True:
            print("FSI iteration {}".format(self.iter))
            self.com.Barrier()

            # Solid to fluid mechanical transfer

            self.clock['Communication'].start()
            self.transferDispSF()
            self.clock['Communication'].end()

            # Fluid solver call for FSI subiteration
            
            printY('Launching fluid solver\n')

            
            ok = None
            self.clock['Fluid run'].start()
            if self.com.rank == 0: ok = self.solverF.run(self.step.time,self.step.nextTime)
            self.clock['Fluid run'].end()

            if self.com.rank == 0: ok = np.repeat(ok,2)
            self.com.Barrier()
            ok = self.com.scatter(ok,root=0)
            self.com.Barrier()

            if not ok: return False
                
            # Fluid to solid mechanical transfer

            self.clock['Communication'].start()
            self.transferLoadFS()
            self.clock['Communication'].end()

            # Solid solver call for FSI subiteration
            
            printY('Launching solid solver\n')

            ok = None
            self.clock['Solid run'].start()
            if self.com.rank == 1: ok = self.solverS.run(self.step.time,self.step.nextTime)
            self.clock['Solid run'].end()

            if self.com.rank == 1: ok = np.repeat(ok,2)
            ok = self.com.scatter(ok,root=1)
            self.com.Barrier()

            if not ok: return False

            # Compute the mechanical residual
            
            if self.com.rank == 1: self.residualDispS()
            self.getResidualDispS() # REMOVE THIS !

            self.converg.update(self.residualS)
            self.logIter.write(self.iter,self.converg.epsilon)
            print('Residual =',self.converg.epsilon)

            # Use BGS relaxation for solid displacement
            
            self.clock['Relax BGS-ADR'].start()
            if self.com.rank == 1: self.relaxation()
            self.clock['Relax BGS-ADR'].end()

            # End of the coupling iteration

            self.iter += 1
            if self.converg.isVerified(): break
            elif self.iter > self.iterMax: return False
        
        return True

# %% BGS Relaxation of Solid Displacement

    def relaxation(self):

        if self.aitken: self.setOmega()
        self.interp.dispS += self.omega*self.residualS

    # Compute omega with Aitken relaxation

    def setOmega(self):

        if self.iter == 0:
            self.omega = max(self.omegaMax,self.omega)

        else:

            dRes = self.residualS-self.prevResidualS
            prodRes = np.sum(dRes*self.prevResidualS)
            dResNormSqr = np.sum(np.linalg.norm(dRes,axis=0)**2)
            if dResNormSqr != 0: self.omega *= -prodRes/dResNormSqr
            else: self.omega = self.omegaMin

        # Changes omega if out of the range

        self.omega = min(self.omega,1)
        self.omega = max(self.omega,self.omegaMin)
        self.prevResidualS = self.residualS.copy()