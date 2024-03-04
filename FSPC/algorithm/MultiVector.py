from mpi4py.MPI import COMM_WORLD as CW
from ..general import Toolbox as tb
from .Algorithm import Algorithm
import numpy as np

# |---------------------------------------------------|
# |   Interface Quasi-Newton Multi-Vector Jacobian    |
# |---------------------------------------------------|

class MVJ(Algorithm):
    def __init__(self,maxIter):

        Algorithm.__init__(self)
        self.maxIter = maxIter
        self.omega = 0.5
        self.BGS = True

# |---------------------------------|
# |   Coupling at Each Time Step    |
# |---------------------------------|

    def couplingAlgo(self):

        self.iteration = 0
        while self.iteration < self.maxIter:

            # Transfer and fluid solver call

            self.transferDirichlet()
            if not self.runFluid(): return False

            # Transfer and solid solver call

            self.transferNeumann()
            if not self.runSolid(): return False

            # Compute the coupling residual

            output = self.relaxation()
            verified = CW.bcast(output,root=1)
            self.BGS = False

            # Exit the loop if the solution is converged

            self.iteration += 1
            if verified: self.__updateJprev(); return True
            self.wayBack()

        self.BGS = True
        return False

# |--------------------------------------|
# |   Compute the Solution Correction    |
# |--------------------------------------|

    def __compute(self,conv):
    
        V = np.flip(np.transpose(conv.V),axis=1)
        W = np.flip(np.transpose(conv.W),axis=1)
        R = np.hstack(-conv.residual)

        # Update the inverse Jacobian

        X = np.transpose(W-np.dot(conv.Jprev,V))
        deltaJ = np.transpose(np.linalg.lstsq(V.T,X,-1)[0])
        conv.J = conv.Jprev+deltaJ

        # Return the solution correction

        delta = np.dot(conv.J,R)-R
        return np.split(delta,tb.Solver.getSize())

# |-----------------------------------------------|
# |   Reset Jacobian and Perform BGS Iteration    |
# |-----------------------------------------------|

    def __reset(self,conv,size):

        conv.J = np.zeros((size,size))
        conv.Jprev = np.zeros((size,size))
        return self.omega*conv.residual

    # Update the previous inverse Jacobian

    @tb.only_solid
    def __updateJprev(self):

        if tb.ResMech:
            tb.ResMech.Jprev = np.copy(tb.ResMech.J)

        if tb.ResTher:
            tb.ResTher.Jprev = np.copy(tb.ResTher.J)

# |-------------------------------------------------|
# |   Relaxation of Solid Interface Displacement    |
# |-------------------------------------------------|

    @tb.conv_mecha
    def updateDisplacement(self):

        disp = tb.Solver.getPosition()

        # Perform either BGS or IQN iteration

        if self.iteration == 0:

            tb.ResMech.V = list()
            tb.ResMech.W = list()
            if self.BGS: delta = self.__reset(tb.ResMech,disp.size)
            else:

                R = np.hstack(-tb.ResMech.residual)
                delta = np.dot(tb.ResMech.Jprev,R)-R
                delta = np.split(delta,tb.Solver.getSize())

        else:

            tb.ResMech.V.append(np.hstack(tb.ResMech.deltaRes()))
            tb.ResMech.W.append(np.hstack(disp-self.prevDisp))
            delta = self.__compute(tb.ResMech)

        # Update the pedicted displacement

        tb.Interp.disp += delta
        self.prevDisp = np.copy(disp)

# |------------------------------------------------|
# |   Relaxation of Solid Interface Temperature    |
# |------------------------------------------------|

    @tb.conv_therm
    def updateTemperature(self):

        temp = tb.Solver.getTemperature()

        # Perform either BGS or IQN iteration

        if self.iteration == 0:

            tb.ResTher.V = list()
            tb.ResTher.W = list()
            if self.BGS: delta = self.__reset(tb.ResTher,temp.size)
            else:

                R = np.hstack(-tb.ResTher.residual)
                delta = np.dot(tb.ResTher.Jprev,R)-R
                delta = np.split(delta,tb.Solver.getSize())

        else:
            
            tb.ResTher.V.append(np.hstack(tb.ResTher.deltaRes()))
            tb.ResTher.W.append(np.hstack(temp-self.prevTemp))
            delta = self.__compute(tb.ResTher)

        # Update the pedicted temperature

        tb.Interp.temp += delta
        self.prevTemp = np.copy(temp)
