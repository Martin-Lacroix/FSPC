from .algorithm import Algorithm
from ..tools import printY,scatterFS,scatterSF
import numpy as np

# %% Interface Quasi-Newton with Inverse Least Squares

class IQN_MVJ(Algorithm):
    def __init__(self,input,param,com):
        Algorithm.__init__(self,input,param,com)

        self.makeBGS = True
        self.dim = param['dim']
        self.omega = param['omega']
        size = self.solver.nbrNode*self.dim
        if com.rank == 1: self.J = np.zeros((size,size))

# %% Coupling at Each Time Step

    def couplingAlgo(self,com):

        verified = False
        self.iteration = 0

        if com.rank == 1:

            self.V = list()
            self.W = list()
            self.Jprev = self.J.copy()
            self.converg.epsilon = np.inf

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

                # Use MVJ relaxation for solid displacement
            
                self.clock['Relax IQN-MVJ'].start()
                self.relaxation()
                self.clock['Relax IQN-MVJ'].end()
            
            # Check the converence of the FSI

            if com.rank == 1: verified = self.converg.isVerified()
            verified = scatterSF(verified,com)

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