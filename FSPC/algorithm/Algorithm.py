from .. import Toolbox as tb
from mpi4py import MPI
import numpy as np
import sys

# %% Parent Algorithm Class

class Algorithm(object):
    def __init__(self,solver):

        self.solver = solver
        self.verified = True
        self.convergM = None
        self.convergT = None
        self.dim = self.solver.dim

# %% Runs the Fluid-Solid Coupling

    @tb.compute_time
    def simulate(self):

        com = MPI.COMM_WORLD
        if com.rank == 1: self.initInterp()
        self.solver.save()

        # Main loop of the FSI partitioned coupling
        
        while self.step.time < self.endTime:

            if com.rank == 1: self.printStep()
            if com.rank == 1: self.predictorStep()
            if self.step.dt < 1e-9: raise Exception('Small time step')
            self.verified = self.couplingAlgo(com)

            # Restart the time step the coupling fails

            if not self.verified:

                if com.rank == 1: self.cancelStep()
                self.step.update(self.verified)
                continue

            # Update the solvers for the next time step

            self.solver.update()
            self.step.update(self.verified)
            if self.step.mustSave(): self.solver.save()

        # Ends the FSI simulation

        com.Barrier()
        self.solver.exit()

# %% Predictor for the Next Solution

    def cancelStep(self):

        if self.convergM: self.interp.pos = np.copy(self.prevMech)
        if self.convergT: self.interp.temp = np.copy(self.prevTher)

    def predictorStep(self):

        if self.convergM: self.predictorM(self.step.dt)
        if self.convergT: self.predictorT(self.step.dt)

    # Mechanical solution predictor

    def predictorM(self,dt):

        if self.verified:
            
            self.prevMech = np.copy(self.interp.pos)
            self.rateMech = self.solver.getVelocity()

        self.interp.pos += dt*self.rateMech

    # Thermal solution predictor

    def predictorT(self,dt):

        if self.verified:
            
            self.prevTher = np.copy(self.interp.temp)
            self.rateTher = self.solver.getTempVeloc()

        self.interp.temp += dt*self.rateTher

# %% Initialization and Relaxation

    def initInterp(self):

        if self.convergM: self.interp.pos = self.solver.getPosition()
        if self.convergT: self.interp.temp = self.solver.getTemperature()

    @tb.compute_time
    def relaxation(self):

        if self.convergM: self.relaxationM()
        if self.convergT: self.relaxationT()
        self.printResidual()

# %% Transfer and Update Functions

    def computeResidual(self):
        
        if self.convergM:
            pos = self.solver.getPosition()
            self.resPos = pos-self.interp.pos

        if self.convergT:
            temp = self.solver.getTemperature()
            self.resTemp = temp-self.interp.temp

    # Transfer Dirichlet data Solid to Fluid

    def transferDirSF(self,com):

        if self.convergM: self.interp.applyDispSF(self.step.dt,com)
        if self.convergT: self.interp.applyTempSF(com)

    # Transfer Neumann data Fluid to Solid

    def transferNeuFS(self,com):

        if self.convergM: self.interp.applyLoadFS(com)
        if self.convergT: self.interp.applyHeatFS(com)

# %% Verification of Convergence

    def resetConverg(self):

        if self.convergM: self.convergM.epsilon = np.inf
        if self.convergT: self.convergT.epsilon = np.inf

    def updateConverg(self):

        if self.convergM: self.convergM.update(self.resPos)
        if self.convergT: self.convergT.update(self.resTemp)

    def isVerified(self):

        verif = list()
        if self.convergM: verif.append(self.convergM.isVerified())
        if self.convergT: verif.append(self.convergT.isVerified())
        return all(verif)

# %% Print Some Informations

    def printResidual(self):

        if self.convergM:

            iter = '[{:.0f}]'.format(self.iteration)
            epsilon = 'Residual Mech : {:.3e}'.format(self.convergM.epsilon)
            print(iter,epsilon)
            sys.stdout.flush()

        if self.convergT:

            iter = '[{:.0f}]'.format(self.iteration)
            epsilon = 'Residual Ther : {:.3e}'.format(self.convergT.epsilon)
            print(iter,epsilon)
            sys.stdout.flush()

    def printStep(self):

        L = '\n------------------------------------------'
        timeStep = 'Time Step : {:.3e}'.format(self.step.dt)
        time = '\nTime : {:.3e}'.format(self.step.time).ljust(20)
        print(L,time,timeStep,L)
        sys.stdout.flush()