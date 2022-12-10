from ..toolbox import compute_time
import numpy as np
import sys

# %% Parent Algorithm Class

class Algorithm(object):
    def __init__(self,solver):

        self.solver = solver
        self.verified = True
        self.dim = self.solver.dim

# %% Runs the Fluid-Solid Coupling

    @compute_time
    def simulate(self,com):

        self.write = np.arange(self.dtWrite,self.endTime,self.dtWrite)
        self.write = np.append(self.write,self.endTime).tolist()
        self.write.append(np.inf)
        self.solver.save()
        
        while self.step.time < self.endTime:

            if com.rank == 1: self.printStep()
            if self.step.dt < 1e-9: raise Exception('Small time step')

            # Save previous time step data

            if (com.rank == 1) and self.verified:

                prevDisp = self.interp.disp.copy()
                velocity = self.solver.getVelocity()

            # Predictor and Internal FSI loop

            dt = self.step.dt
            if com.rank == 1: self.interp.disp += dt*velocity
            self.verified = self.couplingAlgo(com)

            # Restart the time step the coupling fails

            if not self.verified:

                if com.rank == 1: self.interp.disp = prevDisp.copy()
                self.step.update(self.verified)
                continue

            # Update the solvers for the next time step

            self.solver.update()
            self.step.update(self.verified)
            if self.step.time >= self.write[0]:

                self.solver.save()
                self.write.pop(0)

        # Ends the FSI simulation

        com.Barrier()
        self.solver.exit()

# %% Transfer and Update Functions

    def residualDispS(self):

        disp = self.solver.getDisplacement()
        self.residual = disp-self.interp.disp

    # Transfers mechanical data Fluid -> Solid

    def transferLoadFS(self,com):

        nextTime = self.step.timeFrame()[1]
        self.interp.applyLoadFS(nextTime,com)
        
    # Transfers mechanical data Solid -> Fluid

    def transferDispSF(self,com):
        self.interp.applyDispSF(com)

# %% Print Some Informations

    def printStep(self):

        L = '\n------------------------------------------'
        timeStep = 'Time Step : {:.3e}'.format(self.step.dt)
        time = '\nTime : {:.3e}'.format(self.step.time).ljust(20)
        print(L,time,timeStep,L)
        sys.stdout.flush()

    def printRes(self):

        iter = '[{:.0f}]'.format(self.iteration)
        epsilon = 'Residual : {:.3e}'.format(self.converg.epsilon)
        print(iter,epsilon)
        sys.stdout.flush()