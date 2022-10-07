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
            self.Jprev = np.zeros((size,size))
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
            
                self.clock['Relax IQN-MVJ'].start()
                self.relaxation()
                self.clock['Relax IQN-MVJ'].end()
            
            # Check the converence of the FSI

            if com.rank == 1: verified = self.converg.isVerified()
            verified = tools.scatterSF(verified,com)
            self.iteration += 1

            # End of the coupling iteration

            if verified == True:
                if com.rank == 1: self.Jprev = self.J.copy()
                return True

            if self.iteration > self.iterMax:
                if com.rank == 1: self.Jprev.fill(0)
                self.makeBGS = True
                return False

# %% IQN Relaxation of Solid Displacement

    def relaxation(self):

            disp = self.solver.getDisplacement()

            # Performs either BGS or IQN iteration

            if self.makeBGS:

                self.interp.disp += self.omega*self.residual
                self.makeBGS = False

            elif self.iteration == 0:

                R = np.concatenate(self.residual.T)
                correction = np.split(np.dot(self.Jprev,-R)+R,self.dim)
                self.interp.disp += np.transpose(correction)

            else:

                self.V.insert(0,np.concatenate((self.residual-self.prevResidual).T))
                self.W.insert(0,np.concatenate((disp-self.prevDisp).T))
                R = np.concatenate(self.residual.T)
                V = np.transpose(self.V)
                W = np.transpose(self.W)

                # Computes the inverse Jacobian and new displacement

                X = np.transpose(W-np.dot(self.Jprev,V))
                self.J = self.Jprev+np.linalg.lstsq(V.T,X,rcond=-1)[0].T
                correction = np.split(np.dot(self.J,-R)+R,self.dim)
                self.interp.disp += np.transpose(correction)

            # Updates the residuals and displacement

            self.prevDisp = disp.copy()
            self.prevResidual = self.residual.copy()