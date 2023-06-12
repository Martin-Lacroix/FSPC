from .Algorithm import Algorithm
import numpy as np

# %% Interface Quasi-Newton with Multi-Vector Jacobian

class MVJ(Algorithm):
    def __init__(self,solver):
        Algorithm.__init__(self,solver)

        self.makeBGS = True
        self.hasJM = False
        self.hasJT = False

# %% Coupling at Each Time Step

    def couplingAlgo(self,com):

        verif = False
        self.iteration = 0
        timeFrame = self.step.timeFrame()
        self.resetConverg()

        if (com.rank == 1) and self.convergM:

            self.VM = list()
            self.WM = list()

        if (com.rank == 1) and self.convergT:

            self.VT = list()
            self.WT = list()

        while self.iteration < self.maxIter:

            # Transfer and fluid solver call
            
            self.transferDirSF(com)
            if com.rank == 0: verif = self.solver.run(*timeFrame)
            verif = com.scatter([verif,verif],root=0)
            if not verif: return False

            # Transfer and solid solver call

            self.transferNeuFS(com)
            if com.rank == 1: verif = self.solver.run(*timeFrame)
            verif = com.scatter([verif,verif],root=1)
            if not verif: return False

            # Compute the coupling residual

            if com.rank == 1:
                
                self.computeResidual()
                self.updateConverg()
                self.relaxation()
            
            # Check the coupling converence

            if com.rank == 1: verif = self.isVerified()
            verif = com.scatter([verif,verif],root=1)
            self.iteration += 1

            # End of the coupling iteration

            if verif == True:
                 
                if self.hasJM: self.JprevM = np.copy(self.JM)
                if self.hasJT: self.JprevT = np.copy(self.JT)
                return True

        self.makeBGS = True
        return False

# %% Relaxation of Solid Interface Displacement

    def relaxationM(self):

            pos = self.solver.getPosition()

            # Performs either BGS or IQN iteration

            if self.makeBGS:
                
                self.makeBGS = False
                size = self.solver.nbrNode*self.dim
                self.JprevM = np.zeros((size,size))
                self.interp.pos += self.omega*self.resPos

            elif self.iteration == 0:

                R = np.concatenate(self.resPos.T)
                correction = np.split(np.dot(self.JprevM,-R)+R,self.dim)
                self.interp.pos += np.transpose(correction)

            else:

                self.VM.insert(0,np.concatenate((self.resPos-self.prevResM).T))
                self.WM.insert(0,np.concatenate((pos-self.prevPos).T))
                R = np.concatenate(self.resPos.T)
                V = np.transpose(self.VM)
                W = np.transpose(self.WM)

                # Computes the inverse Jacobian and new displacement

                X = np.transpose(W-np.dot(self.JprevM,V))
                self.JM = self.JprevM+np.linalg.lstsq(V.T,X,rcond=-1)[0].T
                correction = np.split(np.dot(self.JM,-R)+R,self.dim)
                self.interp.pos += np.transpose(correction)
                self.hasJM = True

            # Updates the residuals and displacement

            self.prevPos = np.copy(pos)
            self.prevResM = np.copy(self.resPos)

# %% Relaxation of Solid Interface Displacement

    def relaxationT(self):

            temp = self.solver.getTemperature()

            # Performs either BGS or IQN iteration

            if self.makeBGS:
                
                self.makeBGS = False
                size = self.solver.nbrNode
                self.JprevT = np.zeros((size,size))
                self.interp.temp += self.omega*self.resTemp

            elif self.iteration == 0:

                R = np.concatenate(self.resTemp.T)
                correction = np.split(np.dot(self.JprevT,-R)+R,1)
                self.interp.temp += np.transpose(correction)

            else:

                self.VT.insert(0,np.concatenate((self.resTemp-self.prevResT).T))
                self.WT.insert(0,np.concatenate((temp-self.prevTemp).T))
                R = np.concatenate(self.resTemp.T)
                V = np.transpose(self.VT)
                W = np.transpose(self.WT)

                # Computes the inverse Jacobian and new displacement

                X = np.transpose(W-np.dot(self.JprevT,V))
                self.JT = self.JprevT+np.linalg.lstsq(V.T,X,rcond=-1)[0].T
                correction = np.split(np.dot(self.JT,-R)+R,1)
                self.interp.temp += np.transpose(correction)
                self.hasJT = True

            # Updates the residuals and displacement

            self.prevTemp = np.copy(temp)
            self.prevResT = np.copy(self.resTemp)
