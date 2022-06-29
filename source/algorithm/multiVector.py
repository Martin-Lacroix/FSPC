from .algorithm import Algorithm
from .. import tools
import numpy as np

# %% Interface Quasi-Newton with Inverse Least Squares

class IQN_MVJ(Algorithm):
    def __init__(self,input,param,com):
        Algorithm.__init__(self,input,param)

        if com.rank == 1: 

            self.makeBGS = True
            self.omega = param['omega']
            size = self.solver.nbrNode*self.dim
            self.J = np.zeros((size,size))

# %% Coupling at Each Time Step

    def couplingAlgo(self,com):

        verified = False
        self.iteration = 0
        self.converg.epsilon = np.inf
        timeFrame = self.step.timeFrame()

        if com.rank == 1:

            self.V = list()
            self.W = list()
            self.Jprev = self.J.copy()

        while True:

            # Solid to fluid mechanical transfer

            self.clock['Communication'].start()
            self.transferDispSF(com)
            self.clock['Communication'].end()

            # Fluid solver call for FSI subiteration
            
            if com.rank == 0:

                self.clock['Solver run'].start()
                verified = self.log.exec(self.solver.run,*timeFrame)
                self.clock['Solver run'].end()

            verified = tools.scatterFS(verified,com)
            if not verified: return False

            # Fluid to solid mechanical transfer

            self.clock['Communication'].start()
            self.transferLoadFS(com)
            self.clock['Communication'].end()

            # Solid solver call for FSI subiteration
            
            if com.rank == 1:

                self.clock['Solver run'].start()
                verified = self.log.exec(self.solver.run,*timeFrame)
                self.clock['Solver run'].end()

            verified = tools.scatterSF(verified,com)
            if not verified: return False

            # Compute the mechanical residual
            
            if com.rank == 1:
            
                self.residualDispS()
                self.converg.update(self.residual)

                # Print the curent iteration and residual

                iter = 'Iteration : {:.0f}'.format(self.iteration).ljust(20)
                epsilon = 'Residual : {:.3e}'.format(self.converg.epsilon)
                self.logGen.print(iter,epsilon)

                # Use the relaxation for solid displacement
            
                self.clock['Relax IQN-MVJ'].start()
                self.relaxation()
                self.clock['Relax IQN-MVJ'].end()
            
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

            if self.makeBGS:

                self.interp.disp += self.omega*self.residual
                self.makeBGS = False

            elif self.iteration == 0:

                J = self.Jprev.copy()
                np.fill_diagonal(J,J.diagonal()-1)
                R = np.concatenate(self.residual.T)
                correction = np.split(np.dot(J,-R),self.dim)
                self.interp.disp += np.transpose(correction)

            else:

                self.V.insert(0,np.concatenate((self.residual-self.prevResidual).T))
                self.W.insert(0,np.concatenate((disp-self.prevDisp).T))
                R = np.concatenate(self.residual.T)
                V = np.transpose(self.V)
                W = np.transpose(self.W)

                # Computes the inverse Jacobian and new displacement

                Vinv = np.linalg.pinv(V)
                self.J = self.Jprev+np.dot(W-self.Jprev.dot(V),Vinv)

                J = self.J.copy()
                np.fill_diagonal(J,J.diagonal()-1)
                correction = np.split(np.dot(J,-R),self.dim)
                self.interp.disp += np.transpose(correction)

            # Updates the residuals and displacement

            self.prevDisp = disp.copy()
            self.prevResidual = self.residual.copy()