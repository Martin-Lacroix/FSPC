from .. import tools
import collections

# %% Parent Algorithm Class

class Algorithm(object):
    def __init__(self,input,param):
    
        # Data from the input dictionary

        self.step = input['step']
        self.interp = input['interp']
        self.solver = input['solver']

        # Data from the param dictionary

        self.log = param['log']
        self.totTime = param['tTot']
        self.iterMax = param['maxIt']
        self.dtWrite = param['dtWrite']
        self.converg = input['converg']

        # Initialize other simulation data

        self.verified = True
        self.dim = self.solver.dim
        self.logGen = tools.Log('general.log')
        self.clock = collections.defaultdict(tools.Clock)

# %% Runs the Fluid-Solid Coupling

    def run(self,com):

        self.clock['Total time'].start()
        prevWrite = self.step.time
        
        while self.step.time < self.totTime:
            
            # Print the current time step

            if com.rank == 1:

                time = '\nTime : {:.3e}'.format(self.step.time).ljust(20)
                timeStep = 'Time Step : {:.3e}'.format(self.step.dt)
                self.logGen.print(time,timeStep)

            # Save previous time step

            if self.verified is True:

                prevDisp = self.interp.disp.copy()
                prevLoad = self.interp.load.copy()
                if com.rank == 1: self.vel = self.solver.getVelocity()
                if com.rank == 1: self.acc = self.solver.getAcceleration()

            # Predictor and Internal FSI loop

            if com.rank == 1:
                self.interp.disp += self.step.dt*(self.vel+self.acc*self.step.dt/2)
            self.verified = self.couplingAlgo(com)

            # Restart the time step if fail

            if not self.verified:
                
                self.interp.disp = prevDisp.copy()
                self.interp.load = prevLoad.copy()
                self.step.update(self.verified)
                continue

            # Update the F and S solvers for the next time step
            
            self.clock['Solver update'].start()
            self.log.exec(self.solver.update)
            self.clock['Solver update'].end()

            # Write fluid and solid solution
            
            if self.step.time-prevWrite > self.dtWrite:

                self.clock['Solver save'].start()
                self.solver.save()
                self.clock['Solver save'].end()
                prevWrite = self.step.time

            # Update the time step manager class

            self.step.update(self.verified)

        # Ends the FSI simulation

        com.Barrier()
        self.clock['Total time'].end()
        self.log.exec(self.solver.exit)
        tools.timerPrint(self.clock,com)

# %% Transfer and Update Functions

    def residualDispS(self):
        
        disp = self.solver.getDisplacement()
        self.residual = disp-self.interp.disp

    # Transfers mechanical data fluid -> solid

    def transferLoadFS(self,com):

        self.interp.interpLoadFS(com)
        if com.rank == 1: nextTime = self.step.timeFrame()[1]
        if com.rank == 1: self.interp.applyLoadS(nextTime)
        
    # Transfers mechanical data solid -> fluid

    def transferDispSF(self,com):
        
        self.interp.interpDispSF(com)
        if com.rank == 0: self.interp.applyDispF(self.step.dt)
