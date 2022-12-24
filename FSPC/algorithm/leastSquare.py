from ..toolbox import compute_time
from .Algorithm import Algorithm
import numpy as np

# %% Interface Quasi-Newton with Inverse Least Square

class IQN_ILS(Algorithm):
    def __init__(self,solver):
        Algorithm.__init__(self,solver)

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

            # End of the coupling iteration

            if verif: break
            self.iteration += 1
            if self.iteration > self.iterMax: return False

        return True

# %% IQN Relaxation of Solid Displacement

    @compute_time
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
                C = np.linalg.lstsq(np.transpose(self.V),-R,rcond=-1)[0]
                correction = np.split(np.dot(np.transpose(self.W),C)+R,self.dim)
                self.interp.disp += np.transpose(correction)

            # Updates the residuals and displacement

            self.prevDisp = disp.copy()
            self.prevResidual = self.residual.copy()