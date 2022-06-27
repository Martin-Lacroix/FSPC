from ..tools import printY,qrSolve
from ..tools import printY,scatterFS,scatterSF
from .algorithm import Algorithm
import numpy as np

# %% Interface Quasi-Newton with Inverse Least Squares

class IQN_ILS(Algorithm):
    def __init__(self,input,param,com):
        Algorithm.__init__(self,input,param,com)

        self.dim = param['dim']
        self.omega = param['omega']
        self.retainStep = param['retainStep']

        if com.rank == 1:

            self.V = list()
            self.W = list()
            self.nbrCol = list()

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

                # Use ILS relaxation for solid displacement
            
                self.clock['Relax IQN-ILS'].start()
                self.relaxation()
                self.resizeMatrixVW()
                self.clock['Relax IQN-ILS'].end()
            
            # Check the converence of the FSI

            if com.rank == 1: verified = self.converg.isVerified()
            verified = scatterSF(verified,com)

            # End of the coupling iteration

            if verified: break
            self.iteration += 1
            if self.iteration > self.iterMax: return False

        return True

# %% Add and Remove Time Steps From V and W

    def resizeMatrixVW(self):

        if self.retainStep == 0:

            self.V.clear()
            self.W.clear()

        elif self.converg.isVerified():

            self.nbrCol.insert(0,self.iteration)
            if len(self.nbrCol) > self.retainStep:

                self.W = self.W[:(len(self.W)-self.nbrCol[-1])]
                self.V = self.V[:(len(self.V)-self.nbrCol[-1])]
                self.nbrCol.pop()

        elif self.iteration+1 > self.iterMax:
            
            self.W = self.W[self.iteration:]
            self.V = self.V[self.iteration:]

# %% IQN Relaxation of Solid Displacement

    def relaxation(self):

            disp = self.solver.getDisplacement()

            # Performs either BGS or IQN iteration

            if (self.iteration == 0) and (len(self.V) == 0):
                self.interp.disp += self.omega*self.residual

            else:
                if self.iteration > 0:

                    self.V.insert(0,np.concatenate((self.residual-self.prevResidual).T))
                    self.W.insert(0,np.concatenate((disp-self.prevDisp).T))

                # V and W are stored as transpose and list

                R = np.concatenate(self.residual.T)
                C,W = qrSolve(np.transpose(self.V),np.transpose(self.W),R)
                #C = np.linalg.lstsq(np.transpose(self.V),-R,rcond=None)[0]
                correction = np.split(np.dot(W,C).T+R,self.dim)
                self.interp.disp += np.transpose(correction)

            # Updates the residuals and displacement

            self.prevDisp = disp.copy()
            self.prevResidual = self.residual.copy()