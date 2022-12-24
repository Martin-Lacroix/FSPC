from ..toolbox import compute_time
from .Algorithm import Algorithm
import numpy as np

# %% Interface Quasi-Newton with Inverse Least Squares

class IQN_MVJ(Algorithm):
    def __init__(self,solver,com):
        Algorithm.__init__(self,solver)

        if com.rank == 1: 

            self.makeBGS = True
            size = self.solver.nbrNode*self.dim
            self.Jprev = np.zeros((size,size))
            self.J = np.zeros((size,size))

# %% Coupling at Each Time Step

    def couplingAlgo(self,com):

        verif = False
        self.iteration = 0
        self.converg.epsilon = np.inf
        timeFrame = self.step.timeFrame()

        if com.rank == 1:

            self.V = list()
            self.W = list()

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
            
            # Check the coupling converence

            if com.rank == 1: verif = self.converg.isVerified()
            verif = com.scatter([verif,verif],root=1)
            self.iteration += 1

            # End of the coupling iteration

            if verif == True:
                if com.rank == 1: self.Jprev = self.J.copy()
                return True

            if self.iteration > self.iterMax:
                if com.rank == 1: self.Jprev.fill(0)
                self.makeBGS = True
                return False

# %% IQN Relaxation of Solid Displacement

    @compute_time
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