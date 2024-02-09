from mpi4py.MPI import COMM_WORLD as CW
from ..general import Toolbox as tb
import numpy as np

# |-----------------------------|
# |   Parent Algorithm Class    |
# |-----------------------------|

class Algorithm(object):

    def couplingAlgo(self):
        raise Exception('No coupling algorithm defined')
    
    def relaxTemperature(self):
        raise Exception('No thermal relaxation defined')
    
    def relaxDisplacement(self):
        raise Exception('No mechanical relaxation defined')

# |-----------------------------------|
# |   Run the Fluid-Solid Coupling    |
# |-----------------------------------|

    @tb.compute_time
    def simulate(self,endTime):

        verified = True
        tb.solver.save()
        tb.interp.initialize()

        # Main loop of the FSI partitioned coupling
        
        while tb.step.time < endTime:

            self.showTimeStep()
            self.resetConverg()
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
            tb.interp.initialize()

        # Ends the FSI simulation

        CW.Barrier()
        tb.solver.exit()

# |----------------------------------|
# |   Run Solid and Fluid Solvers    |
# |----------------------------------|

    def runFluid(self):

        verified = None
        if CW.rank == 0:
            
            verified = tb.solver.run()
            if not verified: tb.solver.wayBack()

        return CW.bcast(verified,root=0)
    
    def runSolid(self):

        verified = None
        if CW.rank == 1:

            verified = tb.solver.run()
            if not verified: tb.solver.wayBack()

        return CW.bcast(verified,root=1)

# |--------------------------------------------|
# |   Interpolator Functions and Relaxation    |
# |--------------------------------------------|

    @tb.only_solid
    def computePredictor(self,verified):

        tb.interp.predTemperature(verified)
        tb.interp.predDisplacement(verified)

    @tb.only_solid
    def resetConverg(self):

        if tb.convMech: tb.convMech.reset()
        if tb.convTher: tb.convTher.reset()

    # Update the predicted interface solution

    @tb.only_solid
    @tb.compute_time
    def relaxation(self):

        self.computeResidual()
        self.relaxDisplacement()
        self.relaxTemperature()
        self.showResidual()

        # Check for coupling convergence

        verified = list()
        if tb.convMech: verified.append(tb.convMech.verified())
        if tb.convTher: verified.append(tb.convTher.verified())
        return np.all(verified)

# |------------------------------------|
# |   Transfer and Update Functions    |
# |------------------------------------|

    def computeResidual(self):
        
        if tb.convMech:
            disp = tb.solver.getPosition()
            tb.convMech.updateRes(disp,tb.interp.disp)

        if tb.convTher:
            temp = tb.solver.getTemperature()
            tb.convTher.updateRes(temp,tb.interp.temp)

    # Transfer Dirichlet data Solid to Fluid

    def transferDirichletSF(self):

        tb.interp.applyDispSF()
        tb.interp.applyTempSF()

    # Transfer Neumann data Fluid to Solid

    def transferNeumannFS(self):

        tb.interp.applyLoadFS()
        tb.interp.applyHeatFS()

# |------------------------------------|
# |   Print Convergence Information    |
# |------------------------------------|

    def showResidual(self):

        if tb.convMech:

            iter = '[{:.0f}]'.format(self.iteration)
            eps = 'Residual Mech : {:.3e}'.format(tb.convMech.epsilon)
            print(iter,eps)

        if tb.convTher:

            iter = '[{:.0f}]'.format(self.iteration)
            eps = 'Residual Ther : {:.3e}'.format(tb.convTher.epsilon)
            print(iter,eps)

    @tb.only_solid
    def showTimeStep(self):

        L = '\n------------------------------------------'
        timeStep = 'Time Step : {:.3e}'.format(tb.step.dt)
        time = '\nTime : {:.3e}'.format(tb.step.time).ljust(20)
        print(L,time,timeStep,L)
