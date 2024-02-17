from mpi4py.MPI import COMM_WORLD as CW
from ..general import Toolbox as tb
import numpy as np

# |---------------------------------|
# |   Parent FSI Algorithm Class    |
# |---------------------------------|

class Algorithm(object):
    def __init__(self):

        self.hasRun = False

# |-------------------------------------------|
# |   Start the Fluid-Structure Simulation    |
# |-------------------------------------------|

    @tb.compute_time
    def simulate(self,endTime):
        
        verified = True
        tb.solver.save()

        # Main loop on the FSI coupling time steps
        
        while tb.step.time < endTime:
            
            tb.interp.initialize()
            self.displayTimeStep()
            self.resetConverg()

            # Main loop on the FSI coupling iterations

            self.computePredictor(verified)
            verified = self.couplingAlgo()
            tb.step.updateTime(verified)

            # Update the solvers for the next time step

            if verified:

                tb.solver.updateBackup()
                tb.step.updateSave(tb.solver)
                self.hasRun = False

            else: self.solverWayBack(); continue

        # End of the FSI simulation

        CW.Barrier()
        tb.solver.exit()

# |-----------------------------------------|
# |   Run and Restore the Solver Backups    |
# |-----------------------------------------|

    def runFluid(self):

        verified = None
        if CW.rank == 0:
            
            self.hasRun = True
            verified = tb.solver.run()

        return CW.bcast(verified,root=0)
    
    def runSolid(self):

        verified = None
        if CW.rank == 1:
            
            self.hasRun = True
            verified = tb.solver.run()

        return CW.bcast(verified,root=1)
    
    # Reset the solvers to their last backup state

    @tb.write_logs
    @tb.compute_time
    def solverWayBack(self):

        if self.hasRun: tb.solver.wayBack()
        self.hasRun = False

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
        self.displayResidual()

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

    def displayResidual(self):

        if tb.convMech:

            iter = '[{:.0f}]'.format(self.iteration)
            eps = 'Residual Mech : {:.3e}'.format(tb.convMech.epsilon)
            print(iter,eps)

        if tb.convTher:

            iter = '[{:.0f}]'.format(self.iteration)
            eps = 'Residual Ther : {:.3e}'.format(tb.convTher.epsilon)
            print(iter,eps)

    @tb.only_solid
    def displayTimeStep(self):

        L = '\n------------------------------------------'
        timeStep = 'Time Step : {:.3e}'.format(tb.step.dt)
        time = '\nTime : {:.3e}'.format(tb.step.time).ljust(20)
        print(L,time,timeStep,L)
