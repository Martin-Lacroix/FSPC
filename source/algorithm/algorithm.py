from .. import tools
import collections

# %% Parent Algorithm Class

class Algorithm(object):
    def __init__(self,input,param):
    
        # Data from the input dictionary

        self.step = input['step']
        self.interp = input['interp']
        self.solver = input['solver']
        self.converg = input['converg']

        # Data from the param dictionary

        self.log = param['log']
        self.totTime = param['tTot']
        self.iterMax = param['maxIt']
        self.dtWrite = param['dtWrite']

        # Initialize other simulation data

        self.verified = True
        self.dim = self.solver.dim
        self.logGen = tools.LogGen(self)
        self.clock = collections.defaultdict(tools.Clock)

# %% Runs the Fluid-Solid Coupling

    def run(self,com):

        self.clock['Total Time'].start()
        prevWrite = self.step.time
        
        while self.step.time < self.totTime:
            if com.rank == 1: self.logGen.printStep()







            if self.step.dt < 1e-6:
                self.solver.save()
                raise Exception('Small DT')








            # Save previous time step data

            if (com.rank == 1) and self.verified:

                prevDisp = self.interp.disp.copy()
                velocity = self.solver.getVelocity()

            # Predictor and Internal FSI loop

            dt = self.step.dt
            if com.rank == 1: self.interp.disp += dt*velocity
            self.verified = self.couplingAlgo(com)

            # Restart the time step if fail

            if not self.verified:

                if com.rank == 1: self.interp.disp = prevDisp.copy()
                self.step.update(self.verified)
                continue

            # Update the solvers for the next time step
            
            self.clock['Solver Update'].start()
            self.log.exec(self.solver.update)
            self.clock['Solver Update'].end()

            # Write fluid and solid solution
            
            if self.step.time-prevWrite > self.dtWrite:

                self.clock['Solver Save'].start()
                self.log.exec(self.solver.save)
                self.clock['Solver Save'].end()
                prevWrite = self.step.time

            # Update the time step manager class

            self.step.update(self.verified)

        # Ends the FSI simulation

        com.Barrier()
        self.clock['Total Time'].end()
        self.log.exec(self.solver.exit)
        self.logGen.printClock(com)

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
