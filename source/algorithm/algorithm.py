from .. import tools
import collections

import numpy as np

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
        self.endTime = param['tEnd']
        self.iterMax = param['maxIt']

        # Make the time frame for saving results

        dtWrite = param['dtWrite']
        self.write = np.arange(dtWrite,self.endTime,dtWrite)
        self.write = np.append(self.write,self.endTime).tolist()
        self.write.append(np.inf)
        
        # Initialize other simulation data

        self.verified = True
        self.dim = self.solver.dim
        self.logGen = tools.LogGen(self)
        self.clock = collections.defaultdict(tools.Clock)

# %% Runs the Fluid-Solid Coupling

    def run(self,com):

        self.clock['Total Time'].start()
        self.clock['Solver Save'].start()
        self.log.exec(self.solver.save)
        self.clock['Solver Save'].end()
        
        while self.step.time < self.endTime:

            if com.rank == 1: self.logGen.printStep()
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
            
            self.clock['Solver Update'].start()
            self.log.exec(self.solver.update)
            self.clock['Solver Update'].end()

            # Update the time and write the solution

            self.step.update(self.verified)
            if self.step.time >= self.write[0]:

                self.clock['Solver Save'].start()
                self.log.exec(self.solver.save)
                self.clock['Solver Save'].end()
                self.write.pop(0)

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
