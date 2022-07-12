from .algorithm import Algorithm
from .. import tools
import numpy as np

# %% Interface Quasi-Newton with Inverse Least Squares

class IQN_ILS(Algorithm):
    def __init__(self,input,param,com):
        Algorithm.__init__(self,input,param)

        if com.rank == 1:
            self.omega = param['omega']

# %% Coupling at Each Time Step

    def couplingAlgo(self,com):

        verified = False
        self.iteration = 0
        self.converg.epsilon = np.inf
        timeFrame = self.step.timeFrame()

        if com.rank == 1:

            self.V = list()
            self.W = list()

        while True:

            # Solid to fluid mechanical transfer

            self.clock['Communication'].start()
            self.transferDispSF(com)
            self.clock['Communication'].end()

            # Fluid solver call for FSI subiteration
            
            if com.rank == 0:

                self.clock['Solver Run'].start()
                verified = self.log.exec(self.solver.run,*timeFrame)
                self.clock['Solver Run'].end()

            verified = tools.scatterFS(verified,com)
            if not verified: return False

            # Fluid to solid mechanical transfer

            self.clock['Communication'].start()
            self.transferLoadFS(com)
            self.clock['Communication'].end()

            # Solid solver call for FSI subiteration
            
            if com.rank == 1:

                self.clock['Solver Run'].start()
                verified = self.log.exec(self.solver.run,*timeFrame)
                self.clock['Solver Run'].end()

            verified = tools.scatterSF(verified,com)
            if not verified: return False

            # Compute the mechanical residual

            if com.rank == 1:
            
                self.residualDispS()
                self.converg.update(self.residual)
                self.logGen.printRes()

                # Use the relaxation for solid displacement
            
                self.clock['Relax IQN-ILS'].start()
                self.relaxation()
                self.clock['Relax IQN-ILS'].end()
            
            # Check the converence of the FSI

            if com.rank == 1: verified = self.converg.isVerified()
            verified = tools.scatterSF(verified,com)

            # End of the coupling iteration

            if verified: break
            self.iteration += 1
            if self.iteration > self.iterMax: return False

        return True

# %% IQN Relaxation of Solid Displacement

    def relaxation(self):

            disp = self.solver.getDisplacement()

            # Performs either BGS or IQN iteration

            if self.iteration == 0:
                self.interp.disp += self.omega*self.residual

            else:

                self.V.insert(0,np.concatenate((self.residual-self.prevResidual).T))
                self.W.insert(0,np.concatenate((disp-self.prevDisp).T))

                # V and W are stored as transpose and list

                R = np.concatenate(self.residual.T)
                C = np.linalg.lstsq(np.transpose(self.V),-R,rcond=None)[0]
                correction = np.split(np.dot(np.transpose(self.W),C)+R,self.dim)
                self.interp.disp += np.transpose(correction)

            # Updates the residuals and displacement

            self.prevDisp = disp.copy()
            self.prevResidual = self.residual.copy()
