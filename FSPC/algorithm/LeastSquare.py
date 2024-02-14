from mpi4py.MPI import COMM_WORLD as CW
from ..general import Toolbox as tb
from .Algorithm import Algorithm
import numpy as np

# |--------------------------------------------------|
# |   Interface Quasi-Newton Inverse Least Square    |
# |--------------------------------------------------|

class ILS(Algorithm):
    def __init__(self,maxIter):

        Algorithm.__init__(self)
        self.maxIter = maxIter
        self.omega = 0.5

# |---------------------------------|
# |   Coupling at Each Time Step    |
# |---------------------------------|

    def couplingAlgo(self):

        self.iteration = 0
        while self.iteration < self.maxIter:

            # Transfer and fluid solver call

            self.transferDirichletSF()
            if not self.runFluid(): return False

            # Transfer and solid solver call

            self.transferNeumannFS()
            if not self.runSolid(): return False

            # Compute the coupling residual

            output = self.relaxation()
            verified = CW.bcast(output,root=1)

            # Exit the loop if the solution is converged

            self.iteration += 1
            if verified: return True
            else: self.solverWayBack()
        
        return False

# |--------------------------------------|
# |   Compute the Solution Correction    |
# |--------------------------------------|

    def compute(self,conv):
        
        V = np.flip(np.transpose(conv.V),axis=1)
        W = np.flip(np.transpose(conv.W),axis=1)
        R = np.hstack(-conv.residual)

        # Return the solution correction

        delta = np.dot(W,np.linalg.lstsq(V,R,-1)[0])-R
        return np.split(delta,tb.solver.getSize())

# |-------------------------------------------------|
# |   Relaxation of Solid Interface Displacement    |
# |-------------------------------------------------|
    
    @tb.conv_mecha
    def relaxDisplacement(self):

        disp = tb.solver.getPosition()

        # Perform either BGS or IQN iteration

        if self.iteration == 0:

            tb.convMech.V = list()
            tb.convMech.W = list()
            delta = self.omega*tb.convMech.residual

        else:
            tb.convMech.V.append(np.hstack(tb.convMech.deltaRes()))
            tb.convMech.W.append(np.hstack(disp-self.prevDisp))
            delta = self.compute(tb.convMech)

        # Update the pedicted displacement

        tb.interp.disp += delta
        self.prevDisp = np.copy(disp)

# |------------------------------------------------|
# |   Relaxation of Solid Interface Temperature    |
# |------------------------------------------------|

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
