from ..tools import printY,qrSolve
from .algorithm import Algorithm
import numpy as np

# %% Interface Quasi-Newton with Inverse Least Squares

class IQN_ILS(Algorithm):
    def __init__(self,input,param):
        Algorithm.__init__(self,input,param)

        self.V = list()
        self.W = list()
        self.nbrCol = list()
        self.dim = param['dim']
        self.omega = param['omega']
        self.retainStep = param['retainStep']

# %% Coupling at Each Time Step

    def couplingAlgo(self):

        self.iter = 0
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
            ok = self.solverF.run(self.step.time,self.step.nextTime)
            self.clock['Fluid run'].end()
            if not ok: return False

            # Fluid to solid mechanical transfer

            self.clock['Communication'].start()
            self.transferLoadFS()
            self.clock['Communication'].end()

            # Solid solver call for FSI subiteration
            
            printY('Launching solid solver\n')

            self.clock['Solid run'].start()
            ok = self.solverS.run(self.step.time,self.step.nextTime)
            self.clock['Solid run'].end()
            if not ok: return False

            # Compute the mechanical residual
            
            self.residualDispS()
            self.converg.update(self.residualS)
            self.logIter.write(self.iter,self.converg.epsilon)
            print('Residual =',self.converg.epsilon)

            # Newton least squares algorithm

            self.clock['Relax IQN-ILS'].start()
            self.relaxation()
            self.resizeMatrixVW()
            self.clock['Relax IQN-ILS'].end()
            
            # End of the iteration

            self.iter += 1
            if self.converg.isVerified(): break
            elif self.iter > self.iterMax: return False

        return True

# %% Add and Remove Time Steps From V and W

    def resizeMatrixVW(self):

        if self.retainStep == 0:

            self.V.clear()
            self.W.clear()

        elif self.converg.isVerified():

            self.nbrCol.insert(0,self.iter)
            if len(self.nbrCol) > self.retainStep:

                self.W = self.W[:(len(self.W)-self.nbrCol[-1])]
                self.V = self.V[:(len(self.V)-self.nbrCol[-1])]
                self.nbrCol.pop()

        elif self.iter+1 > self.iterMax:
            
            self.W = self.W[self.iter:]
            self.V = self.V[self.iter:]

# %% IQN Relaxation of Solid Displacement

    def relaxation(self):

            dispS = self.solverS.getDisplacement()

            # Performs either BGS or IQN iteration

            if (self.iter == 0) and (len(self.V) == 0):
                self.interp.dispS += self.omega*self.residualS

            else:
                if self.iter > 0:

                    self.V.insert(0,np.concatenate((self.residualS-self.prevResidualS).T))
                    self.W.insert(0,np.concatenate((dispS-self.prevDispS).T))

                # V and W are stored as transpose and list

                R = np.concatenate(self.residualS.T)
                C,W = qrSolve(np.transpose(self.V),np.transpose(self.W),R)
                #C = np.linalg.lstsq(np.transpose(self.V),-R,rcond=None)[0]
                correction = np.split(np.dot(W,C).T+R,self.dim)
                self.interp.dispS += np.transpose(correction)

            # Updates the residuals and displacement

            self.prevDispS = dispS.copy()
            self.prevResidualS = self.residualS.copy()