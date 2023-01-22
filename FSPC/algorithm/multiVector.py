from .Algorithm import Algorithm
import numpy as np

# %% Interface Quasi-Newton with Multi-Vector Jacobian

class IQN_MVJ(Algorithm):
    def __init__(self,solver):
        Algorithm.__init__(self,solver)

        self.makeBGS = True

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

        while True:

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

            self.makeBGS = False
            if verif == True:

                if (com.rank == 1) and self.convergM:
                    self.JprevM = np.copy(self.JM)

                if (com.rank == 1) and self.convergT:
                    self.JprevT = np.copy(self.JT)

                return True

            if self.iteration > self.maxIter:
                self.makeBGS = True
                return False

# %% Relaxation of Solid Interface Displacement

    def relaxationM(self):

            disp = self.solver.getDisplacement()

            # Performs either BGS or IQN iteration

            if self.makeBGS:

                size = self.solver.nbrNode*self.dim
                self.JprevM = np.zeros((size,size))
                self.interp.disp += self.omega*self.resDisp

            elif self.iteration == 0:

                R = np.concatenate(self.resDisp.T)
                correction = np.split(np.dot(self.JprevM,-R)+R,self.dim)
                self.interp.disp += np.transpose(correction)

            else:

                self.VM.insert(0,np.concatenate((self.resDisp-self.prevResM).T))
                self.WM.insert(0,np.concatenate((disp-self.prevDisp).T))
                R = np.concatenate(self.resDisp.T)
                V = np.transpose(self.VM)
                W = np.transpose(self.WM)

                # Computes the inverse Jacobian and new displacement

                X = np.transpose(W-np.dot(self.JprevM,V))
                self.JM = self.JprevM+np.linalg.lstsq(V.T,X,rcond=-1)[0].T
                correction = np.split(np.dot(self.JM,-R)+R,self.dim)
                self.interp.disp += np.transpose(correction)

            # Updates the residuals and displacement

            self.prevDisp = np.copy(disp)
            self.prevResM = np.copy(self.resDisp)

# %% Relaxation of Solid Interface Displacement

    def relaxationT(self):

            temp = self.solver.getTemperature()

            # Performs either BGS or IQN iteration

            if self.makeBGS:
                
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

            # Updates the residuals and displacement

            self.prevTemp = np.copy(temp)
            self.prevResT = np.copy(self.resTemp)