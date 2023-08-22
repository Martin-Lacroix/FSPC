from mpi4py.MPI import COMM_WORLD as CW
from ..general import Toolbox as tb
from .Algorithm import Algorithm
import numpy as np

# %% Interface Quasi-Newton with Inverse Least Square

class ILS(Algorithm):
    def __init__(self):

        Algorithm.__init__(self)
        self.omega = 0.5

# %% Coupling at Each Time Step

    def couplingAlgo(self):

        verif = False
        self.iteration = 0
        self.resetConverg()

        while self.iteration < self.maxIter:

            # Transfer and fluid solver call

            self.transferDirichletSF()
            if CW.rank == 0: verif = tb.solver.run()
            verif = CW.scatter([verif,verif],root=0)
            if not verif: return False

            # Transfer and solid solver call

            self.transferNeumannFS()
            if CW.rank == 1: verif = tb.solver.run()
            verif = CW.scatter([verif,verif],root=1)
            if not verif: return False

            # Compute the coupling residual

            verif = self.relaxation()
            verif = CW.scatter([verif,verif],root=1)

            # End of the coupling iteration

            self.iteration += 1
            if verif: return True
            
        return False

# %% Compute the Solution Correction

    def compute(self,conv):
        
        V = np.flip(np.transpose(conv.V),axis=1)
        W = np.flip(np.transpose(conv.W),axis=1)
        R = np.hstack(-conv.residual)

        # Return the solution correction

        delta = np.dot(W,np.linalg.lstsq(V,R,-1)[0])-R
        return np.split(delta,tb.solver.nbrNod)

# %% Relaxation of Solid Interface Displacement
    
    @tb.conv_mecha
    def relaxPosition(self):

        pos = tb.solver.getPosition()

        # Perform either BGS or IQN iteration

        if self.iteration == 0:

            tb.convMech.V = list()
            tb.convMech.W = list()
            delta = self.omega*tb.convMech.residual

        else:
            tb.convMech.V.append(np.hstack(tb.convMech.deltaRes()))
            tb.convMech.W.append(np.hstack(pos-self.prevPos))
            delta = self.compute(tb.convMech)

        # Update the pedicted displacement

        tb.interp.pos += delta
        self.prevPos = np.copy(pos)

# %% Relaxation of Solid Interface Temperature

    @tb.conv_therm
    def relaxTemperature(self):

        temp = tb.solver.getTemperature()

        # Perform either BGS or IQN iteration

        if self.iteration == 0:

            tb.convTher.V = list()
            tb.convTher.W = list()
            delta = self.omega*tb.convTher.residual

        else:
            tb.convTher.V.append(np.hstack(tb.convTher.deltaRes()))
            tb.convTher.W.append(np.hstack(temp-self.prevTemp))
            delta = self.compute(tb.convTher)

        # Update the predicted temperature

        tb.interp.temp += delta
        self.prevTemp = np.copy(temp)
