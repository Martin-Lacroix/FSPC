from .Algorithm import Algorithm
import numpy as np

# %% Interface Quasi-Newton with Inverse Least Square

class ILS(Algorithm):
    def __init__(self,solver):
        Algorithm.__init__(self,solver)

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

            if verif: break
            if self.iteration > self.maxIter: return False

        return True

# %% Relaxation of Solid Interface Displacement

    def relaxationM(self):

        pos = self.solver.getPosition()

        # Performs either BGS or IQN iteration

        if self.iteration == 0:
            self.interp.pos += self.omega*self.resPos

        else:

            self.VM.insert(0,np.concatenate((self.resPos-self.prevResM).T))
            self.WM.insert(0,np.concatenate((pos-self.prevPos).T))

            # V and W are stored as transpose and list

            R = np.concatenate(self.resPos.T)
            C = np.linalg.lstsq(np.transpose(self.VM),-R,rcond=-1)[0]
            correction = np.split(np.dot(np.transpose(self.WM),C)+R,self.dim)
            self.interp.pos += np.transpose(correction)

        # Updates the residuals and displacement

        self.prevPos = np.copy(pos)
        self.prevResM = np.copy(self.resPos)

# %% Relaxation of Solid Interface Temperature

    def relaxationT(self):

        temp = self.solver.getTemperature()

        # Performs either BGS or IQN iteration

        if self.iteration == 0:
            self.interp.temp += self.omega*self.resTemp

        else:

            self.VT.insert(0,np.concatenate((self.resTemp-self.prevResT).T))
            self.WT.insert(0,np.concatenate((temp-self.prevTemp).T))

            # V and W are stored as transpose and list

            R = np.concatenate(self.resTemp.T)
            C = np.linalg.lstsq(np.transpose(self.VT),-R,rcond=-1)[0]
            correction = np.split(np.dot(np.transpose(self.WT),C)+R,1)
            self.interp.temp += np.transpose(correction)

        # Updates the residuals and displacement

        self.prevTemp = np.copy(temp)
        self.prevResT = np.copy(self.resTemp)
