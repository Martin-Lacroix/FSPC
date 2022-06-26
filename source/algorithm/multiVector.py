from ..tools import printY
from .algorithm import Algorithm
import numpy as np

# %% Interface Quasi-Newton with Inverse Least Squares

class IQN_MVJ(Algorithm):
    def __init__(self,input,param):
        Algorithm.__init__(self,input,param)

        self.makeBGS = True
        self.dim = param['dim']
        self.omega = param['omega']
        size = self.solver.nbrNode*self.dim
        self.J = np.zeros((size,size))

# %% Coupling at Each Time Step

    def couplingAlgo(self):

        self.iter = 0
        self.V = list()
        self.W = list()
        self.Jprev = self.J.copy()
        self.converg.epsilon = np.inf

        while True:
            print("FSI iteration {}".format(self.iter))

            # Solid to fluid mechanical transfer

            self.clock['Communication'].start()
            self.transferDispSF()
            self.clock['Communication'].end()

            # Fluid solver call for FSI subiteration
            
            printY('Launching fluid solver\n')

            self.clock['Fluid run'].start()
            ok = self.solver.run(self.step.time,self.step.nextTime)
            self.clock['Fluid run'].end()
            if not ok: return False

            # Fluid to solid mechanical transfer

            self.clock['Communication'].start()
            self.transferLoadFS()
            self.clock['Communication'].end()

            # Solid solver call for FSI subiteration
            
            printY('Launching solid solver\n')

            self.clock['Solid run'].start()
            ok = self.solver.run(self.step.time,self.step.nextTime)
            self.clock['Solid run'].end()
            if not ok: return False

            # Compute the mechanical residual
            
            self.residualDispS()
            self.converg.update(self.residual)
            self.logIter.write(self.iter,self.converg.epsilon)
            print('Residual =',self.converg.epsilon)

            # Newton least squares algorithm

            self.clock['Relax IQN-MVJ'].start()
            self.relaxation()
            self.clock['Relax IQN-MVJ'].end()
            
            # End of the iteration
            
            self.iter += 1
            if self.converg.isVerified(): break
            elif self.iter > self.iterMax: return False

        return True

# %% IQN Relaxation of Solid Displacement

    def relaxation(self):

            dispS = self.solver.getDisplacement()

            # Performs either BGS or IQN iteration

            if self.makeBGS:

                self.interp.disp += self.omega*self.residual
                self.makeBGS = False

            elif (self.iter == 0):

                J = self.Jprev.copy()
                np.fill_diagonal(J,J.diagonal()-1)
                R = np.concatenate(self.residual.T)
                correction = np.split(np.dot(J,-R),self.dim)
                self.interp.disp += np.transpose(correction)

            else:

                self.V.insert(0,np.concatenate((self.residual-self.prevResidual).T))
                self.W.insert(0,np.concatenate((dispS-self.prevDisp).T))
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

            self.prevDisp = dispS.copy()
            self.prevResidual = self.residual.copy()