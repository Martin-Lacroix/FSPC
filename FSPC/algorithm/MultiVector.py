from mpi4py.MPI import COMM_WORLD as CW
from .Algorithm import Algorithm
from .. import Toolbox as tb
from .. import Manager as mg
import numpy as np

# %% Interface Quasi-Newton with Multi-Vector Jacobian

class MVJ(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)
        
        self.makeBGS = True
        self.hasJP = False
        self.hasJT = False

# %% Coupling at Each Time Step

    def couplingAlgo(self):

        verif = False
        self.iteration = 0
        self.resetConverg()

        if (CW.rank == 1) and mg.convMecha:

            self.VP = list()
            self.WP = list()

        if (CW.rank == 1) and mg.convTherm:

            self.VT = list()
            self.WT = list()

        while self.iteration < self.maxIter:

            # Transfer and fluid solver call
            
            self.transferDirichletSF()
            if CW.rank == 0: verif = mg.solver.run()
            verif = CW.scatter([verif,verif],root=0)
            if not verif: return False

            # Transfer and solid solver call

            self.transferNeumannFS()
            if CW.rank == 1: verif = mg.solver.run()
            verif = CW.scatter([verif,verif],root=1)
            if not verif: return False

            # Compute the coupling residual

            self.computeResidual()
            self.updateConverg()
            self.relaxation()
            
            # Check the coupling converence

            verif = self.verified()
            verif = CW.scatter([verif,verif],root=1)
            self.iteration += 1

            # End of the coupling iteration

            if verif == True:
                 
                if self.hasJP: self.JprevP = np.copy(self.JP)
                if self.hasJT: self.JprevT = np.copy(self.JT)
                return True

        self.makeBGS = True
        return False

# %% Relaxation of Solid Interface Displacement

    @tb.only_mecha
    def relaxationM(self):

        pos = mg.solver.getPosition()

        # Performs either BGS or IQN iteration

        if self.makeBGS:

            mg.interp.pos += self.omega*self.resP
            size = mg.solver.nbrNode*mg.solver.dim
            self.JprevP = np.zeros((size,size))
            self.makeBGS = False

        elif self.iteration == 0:

            R = np.hstack(-self.resP.T)
            delta = np.split(np.dot(self.JprevP,R)-R,mg.solver.dim)
            mg.interp.pos += np.transpose(delta)

        else:

            self.VP.insert(0,np.hstack(self.resP.T-self.prevResP.T))
            self.WP.insert(0,np.hstack(pos.T-self.prevPos.T))

            # V and W are stored as transpose and list

            R = np.hstack(-self.resP.T)
            V = np.transpose(self.VP)
            W = np.transpose(self.WP)

            # Computes the inverse Jacobian and new displacement

            X = np.transpose(W-np.dot(self.JprevP,V))
            self.JP = self.JprevP+np.linalg.lstsq(V.T,X,-1)[0].T
            delta = np.split(np.dot(self.JP,R)-R,mg.solver.dim)
            mg.interp.pos += np.transpose(delta)
            self.hasJP = True

        # Updates the residuals and displacement

        self.prevPos = np.copy(pos)
        self.prevResP = np.copy(self.resP)

# %% Relaxation of Solid Interface Displacement

    @tb.only_therm
    def relaxationT(self):

        temp = mg.solver.getTemperature()

        # Performs either BGS or IQN iteration

        if self.makeBGS:

            self.makeBGS = False
            size = mg.solver.nbrNode
            self.JprevT = np.zeros((size,size))
            mg.interp.temp += self.omega*self.resT

        elif self.iteration == 0:

            R = np.hstack(-self.resT.T)
            delta = np.split(np.dot(self.JprevT,R)-R,1)
            mg.interp.temp += np.transpose(delta)

        else:

            self.VT.insert(0,np.hstack((self.resT-self.prevResT).T))
            self.WT.insert(0,np.hstack((temp-self.prevTemp).T))

            # V and W are stored as transpose and list

            R = np.hstack(-self.resT.T)
            V = np.transpose(self.VT)
            W = np.transpose(self.WT)

            # Computes the inverse Jacobian and new displacement

            X = np.transpose(W-np.dot(self.JprevT,V))
            self.JT = self.JprevT+np.linalg.lstsq(V.T,X,-1)[0].T
            delta = np.split(np.dot(self.JT,R)-R,1)
            mg.interp.temp += np.transpose(delta)
            self.hasJT = True

        # Updates the residuals and displacement

        self.prevTemp = np.copy(temp)
        self.prevResT = np.copy(self.resT)
