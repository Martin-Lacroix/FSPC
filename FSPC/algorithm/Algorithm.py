from mpi4py.MPI import COMM_WORLD as CW
from .. import Toolbox as tb
from .. import Manager as mg
import numpy as np

# %% Parent Algorithm Class

class Algorithm(object):

    def couplingAlgo():
        raise Exception('No coupling algorithm defined')

# %% Runs the Fluid-Solid Coupling

    @tb.compute_time
    def simulate(self):

        mg.solver.save()
        verified = True

        # Main loop of the FSI partitioned coupling
        
        while mg.step.time < self.endTime:

            self.showTimeStep()
            self.computePredictor(verified)
            verified = self.couplingAlgo()

            # Restart the time step the coupling fails

            if not verified:

                mg.step.updateTime(verified)
                continue

            # Update the solvers for the next time step

            mg.solver.update()
            mg.step.updateTime(verified)
            mg.step.updateSave(mg.solver)

        # Ends the FSI simulation

        CW.Barrier()
        mg.solver.exit()

# %% Interpolator Functions and Relaxation

    @tb.only_solid
    def computePredictor(self,verif):
        
        mg.interp.predicTerm(verif)
        mg.interp.predicMecha(verif)

    @tb.only_solid
    @tb.compute_time
    def relaxation(self):

        self.relaxationM()
        self.relaxationT()
        self.showResidual()

# %% Transfer and Update Functions

    @tb.only_solid
    def computeResidual(self):
        
        if mg.convMecha:
            pos = mg.solver.getPosition()
            self.resP = pos-mg.interp.pos

        if mg.convTherm:
            temp = mg.solver.getTemperature()
            self.resT = temp-mg.interp.temp

    # Transfer Dirichlet data Solid to Fluid

    def transferDirichletSF(self):

        mg.interp.applyDispSF()
        mg.interp.applyTempSF()

    # Transfer Neumann data Fluid to Solid

    def transferNeumannFS(self):

        mg.interp.applyLoadFS()
        mg.interp.applyHeatFS()

# %% Verification of Convergence

    @tb.only_solid
    def resetConverg(self):

        if mg.convMecha: mg.convMecha.epsilon = np.inf
        if mg.convTherm: mg.convTherm.epsilon = np.inf

    @tb.only_solid
    def updateConverg(self):

        if mg.convMecha: mg.convMecha.update(self.resP)
        if mg.convTherm: mg.convTherm.update(self.resT)

    @tb.only_solid
    def verified(self):

        verif = list()
        if mg.convMecha: verif.append(mg.convMecha.verified())
        if mg.convTherm: verif.append(mg.convTherm.verified())
        return all(verif)

# %% Print Some Informations

    def showResidual(self):

        if mg.convMecha:

            iter = '[{:.0f}]'.format(self.iteration)
            epsilon = 'Residual Mech : {:.3e}'.format(mg.convMecha.epsilon)
            print(iter,epsilon)

        if mg.convTherm:

            iter = '[{:.0f}]'.format(self.iteration)
            epsilon = 'Residual Ther : {:.3e}'.format(mg.convTherm.epsilon)
            print(iter,epsilon)

    @tb.only_solid
    def showTimeStep(self):

        L = '\n------------------------------------------'
        timeStep = 'Time Step : {:.3e}'.format(mg.step.dt)
        time = '\nTime : {:.3e}'.format(mg.step.time).ljust(20)
        print(L,time,timeStep,L)