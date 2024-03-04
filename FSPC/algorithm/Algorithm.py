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
        tb.Solver.save()

        # Main loop on the FSI coupling time steps
        
        while tb.Step.time < endTime:
            
            tb.Interp.initialize()
            self.__displayTimeStep()
            self.__resetConverg()

            # Main loop on the FSI coupling iterations

            self.__computePredictor(verified)
            verified = self.couplingAlgo()
            tb.Step.updateTime(verified)

            # Update the solvers for the next time step

            if verified:

                tb.Solver.update()
                tb.Step.updateSave(tb.Solver)
                self.hasRun = False

            else: self.wayBack(); continue

        # End of the FSI simulation

        CW.Barrier()
        tb.Solver.exit()

# |-----------------------------------------|
# |   Run and Restore the Solver Backups    |
# |-----------------------------------------|

    def runFluid(self):

        verified = None
        if CW.rank == 0:
            
            self.hasRun = True
            verified = tb.Solver.run()

        return CW.bcast(verified,root=0)
    
    def runSolid(self):

        verified = None
        if CW.rank == 1:
            
            self.hasRun = True
            verified = tb.Solver.run()

        return CW.bcast(verified,root=1)
    
    # Reset the solvers to their last backup state

    @tb.write_logs
    @tb.compute_time
    def wayBack(self):

        if self.hasRun: tb.Solver.wayBack()
        self.hasRun = False

# |--------------------------------------------|
# |   Interpolator Functions and Relaxation    |
# |--------------------------------------------|

    @tb.only_solid
    def __computePredictor(self,verified):

        tb.Interp.predTemperature(verified)
        tb.Interp.predDisplacement(verified)

    @tb.only_solid
    def __resetConverg(self):

        if tb.ResMech: tb.ResMech.reset()
        if tb.ResTher: tb.ResTher.reset()

    # Update the predicted interface solution

    @tb.only_solid
    @tb.compute_time
    def relaxation(self):

        self.computeResidual()
        self.updateDisplacement()
        self.updateTemperature()
        self.__displayResidual()

        # Check for coupling convergence

        verified = list()
        if tb.ResMech: verified.append(tb.ResMech.verified())
        if tb.ResTher: verified.append(tb.ResTher.verified())
        return np.all(verified)

# |------------------------------------|
# |   Transfer and Update Functions    |
# |------------------------------------|

    def computeResidual(self):
        
        if tb.ResMech:
            disp = tb.Solver.getPosition()
            tb.ResMech.updateRes(disp,tb.Interp.disp)

        if tb.ResTher:
            temp = tb.Solver.getTemperature()
            tb.ResTher.updateRes(temp,tb.Interp.temp)

    # Transfer Dirichlet data Solid to Fluid

    def transferDirichlet(self):

        tb.Interp.applyDispSF()
        tb.Interp.applyTempSF()

    # Transfer Neumann data Fluid to Solid

    def transferNeumann(self):

        tb.Interp.applyLoadFS()
        tb.Interp.applyHeatFS()

# |------------------------------------|
# |   Print Convergence Information    |
# |------------------------------------|

    def __displayResidual(self):

        if tb.ResMech:

            iter = '[{:.0f}]'.format(self.iteration)
            eps = 'Residual Mech : {:.3e}'.format(tb.ResMech.epsilon)
            print(iter,eps)

        if tb.ResTher:

            iter = '[{:.0f}]'.format(self.iteration)
            eps = 'Residual Ther : {:.3e}'.format(tb.ResTher.epsilon)
            print(iter,eps)

    @tb.only_solid
    def __displayTimeStep(self):

        L = '\n------------------------------------------'
        timeStep = 'Time Step : {:.3e}'.format(tb.Step.dt)
        time = '\nTime : {:.3e}'.format(tb.Step.time).ljust(20)
        print(L,time,timeStep,L)
