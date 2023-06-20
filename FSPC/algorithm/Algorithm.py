from mpi4py.MPI import COMM_WORLD as CW
from .. import Toolbox as tb
import numpy as np

# %% Parent Algorithm Class

class Algorithm(object):

    def couplingAlgo():
        raise Exception('No coupling algorithm defined')

# %% Runs the Fluid-Solid Coupling

    @tb.compute_time
    def simulate(self):

        tb.solver.save()
        verified = True

        # Main loop of the FSI partitioned coupling
        
        while tb.step.time < self.endTime:

            self.showTimeStep()
            self.computePredictor(verified)
            verified = self.couplingAlgo()

            # Restart the time step the coupling fails

            if not verified:

                tb.step.updateTime(verified)
                continue

            # Update the solvers for the next time step

            tb.solver.update()
            tb.step.updateTime(verified)
            tb.step.updateSave(tb.solver)

        # Ends the FSI simulation

        CW.Barrier()
        tb.solver.exit()

# %% Interpolator Functions and Relaxation

    @tb.only_solid
    def computePredictor(self,verif):
        
        tb.interp.predicTerm(verif)
        tb.interp.predicMecha(verif)

    @tb.only_solid
    @tb.compute_time
    def relaxation(self):

        self.relaxationM()
        self.relaxationT()
        self.showResidual()

# %% Transfer and Update Functions

    @tb.only_solid
    def computeResidual(self):
        
        if tb.convMecha:
            pos = tb.solver.getPosition()
            self.resP = pos-tb.interp.pos

        if tb.convTherm:
            temp = tb.solver.getTemperature()
            self.resT = temp-tb.interp.temp

    # Transfer Dirichlet data Solid to Fluid

    def transferDirichletSF(self):

        tb.interp.applyDispSF()
        tb.interp.applyTempSF()

    # Transfer Neumann data Fluid to Solid

    def transferNeumannFS(self):

        tb.interp.applyLoadFS()
        tb.interp.applyHeatFS()

# %% Verification of Convergence

    @tb.only_solid
    def resetConverg(self):

        if tb.convMecha: tb.convMecha.epsilon = np.inf
        if tb.convTherm: tb.convTherm.epsilon = np.inf

    @tb.only_solid
    def updateConverg(self):

        if tb.convMecha: tb.convMecha.update(self.resP)
        if tb.convTherm: tb.convTherm.update(self.resT)

    @tb.only_solid
    def verified(self):

        verif = list()
        if tb.convMecha: verif.append(tb.convMecha.verified())
        if tb.convTherm: verif.append(tb.convTherm.verified())
        return all(verif)

# %% Print Some Informations

    def showResidual(self):

        if tb.convMecha:

            iter = '[{:.0f}]'.format(self.iteration)
            epsilon = 'Residual Mech : {:.3e}'.format(tb.convMecha.epsilon)
            print(iter,epsilon)

        if tb.convTherm:

            iter = '[{:.0f}]'.format(self.iteration)
            epsilon = 'Residual Ther : {:.3e}'.format(tb.convTherm.epsilon)
            print(iter,epsilon)

    @tb.only_solid
    def showTimeStep(self):

        L = '\n------------------------------------------'
        timeStep = 'Time Step : {:.3e}'.format(tb.step.dt)
        time = '\nTime : {:.3e}'.format(tb.step.time).ljust(20)
        print(L,time,timeStep,L)