from mpi4py.MPI import COMM_WORLD as CW
from ..general import Toolbox as tb
import numpy as np

# %% Parent Algorithm Class

class Algorithm(object):

    def couplingAlgo(self):
        raise Exception('No coupling algorithm defined')
    
    def relaxTherm(self):
        raise Exception('No thermal relaxation defined')
    
    def relaxMecha(self):
        raise Exception('No mechanical relaxation defined')

# %% Runs the Fluid-Solid Coupling

    @tb.compute_time
    def simulate(self):

        verified = True
        tb.solver.save()
        tb.interp.initialize()

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
        
        tb.interp.predicTherm(verif)
        tb.interp.predicMecha(verif)

    @tb.only_solid
    @tb.compute_time
    def relaxation(self):

        self.computeResidual()
        self.relaxMecha()
        self.relaxTherm()
        self.showResidual()
        return self.verified()

# %% Transfer and Update Functions

    def computeResidual(self):
        
        if tb.convMech:
            pos = tb.solver.getPosition()
            tb.convMech.updateRes(pos-tb.interp.pos)

        if tb.convTher:
            temp = tb.solver.getTemperature()
            tb.convTher.updateRes(temp-tb.interp.temp)

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

        if tb.convMech: tb.convMech.reset()
        if tb.convTher: tb.convTher.reset()

    def verified(self):

        verif = list()
        if tb.convMech: verif.append(tb.convMech.verified())
        if tb.convTher: verif.append(tb.convTher.verified())
        return np.all(verif)

# %% Print Some Informations

    def showResidual(self):

        if tb.convMech:

            iter = '[{:.0f}]'.format(self.iteration)
            epsilon = 'Residual Mech : {:.3e}'.format(tb.convMech.epsilon)
            print(iter,epsilon)

        if tb.convTher:

            iter = '[{:.0f}]'.format(self.iteration)
            epsilon = 'Residual Ther : {:.3e}'.format(tb.convTher.epsilon)
            print(iter,epsilon)

    @tb.only_solid
    def showTimeStep(self):

        L = '\n------------------------------------------'
        timeStep = 'Time Step : {:.3e}'.format(tb.step.dt)
        time = '\nTime : {:.3e}'.format(tb.step.time).ljust(20)
        print(L,time,timeStep,L)