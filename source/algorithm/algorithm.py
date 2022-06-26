from ..tools import printY,printG,Logs,Clock,timerPrint
import collections

# %% Parent Algorithm Class

class Algorithm(object):
    def __init__(self,input,param,com):

        printY('Initializing FSI algorithm\n')
        
        self.ok = True
        self.com = com
        self.dim = param['dim']

        self.step = input['step']
        self.interp = input['interp']

        if com.rank == 1: self.converg = input['converg']
        if com.rank == 0: self.solverF = input['solverF']
        if com.rank == 1: self.solverS = input['solverS']

        self.clock = collections.defaultdict(Clock)
        self.logTime = Logs('Iteration.log',['Time','Time Step'])
        self.logIter = Logs('Iteration.log',['Iteration','Residual'])

        self.totTime = param['tTot']
        self.iterMax = param['maxIt']
        self.dtWrite = param['dtWrite']

# %% Runs the Fluid-Solid Coupling

    def run(self):

        print('Begin FSI Computation')
        self.clock['Total time'].start()
        prevWrite = self.step.time

        # External temporal loop
        
        while self.step.time < self.totTime:

            self.com.Barrier()

            printG('FSPC: t =',self.step.time,'| dt =',self.step.dt)

            self.logTime.newLine()
            self.interp.logForce.newLine()
            self.logTime.write(self.step.time,self.step.dt)

            # Save previous time step

            if self.ok is True:

                if self.com.rank == 0: prevDispF = self.interp.dispF.copy()
                if self.com.rank == 1: prevDispS = self.interp.dispS.copy()
                if self.com.rank == 0: prevLoadF = self.interp.loadF.copy()
                if self.com.rank == 1: prevLoadS = self.interp.loadS.copy()

                if self.com.rank == 1: self.velS = self.solverS.getVelocity()
                if self.com.rank == 1: self.accS = self.solverS.getAcceleration()

            # Predictor and Internal FSI loop

            if self.com.rank == 1: self.interp.dispS += self.step.dt*(self.velS+self.accS*self.step.dt/2)
            self.ok = self.couplingAlgo()

            # Restart the time step if fail

            if not self.ok:
                
                if self.com.rank == 0: self.interp.dispF = prevDispF.copy()
                if self.com.rank == 1: self.interp.dispS = prevDispS.copy()
                if self.com.rank == 0: self.interp.loadF = prevLoadF.copy()
                if self.com.rank == 1: self.interp.loadS = prevLoadS.copy()

                self.step.update(self.ok)
                continue

            # Update the F and S solvers for the next time step
            
            self.clock['Solid update'].start()
            if self.com.rank == 1: self.solverS.update()
            self.clock['Solid update'].end()

            self.clock['Fluid update'].start()
            if self.com.rank == 0: self.solverF.update()
            self.clock['Fluid update'].end()

            # Write fluid and solid solution
            
            if self.step.time-prevWrite > self.dtWrite:

                self.clock['Fluid save'].start()
                if self.com.rank == 0: self.solverF.save()
                self.clock['Fluid save'].end()

                self.clock['Solid save'].start()
                if self.com.rank == 1: self.solverS.save()
                self.clock['Solid save'].end()

                prevWrite = self.step.time

            # Displacement predictor for next time step and update the S solution

            self.step.update(self.ok)
            self.com.Barrier()

        # Ends the simulation

        if self.com.rank == 1: self.solverS.exit()
        if self.com.rank == 0: self.solverF.exit()

        self.clock['Total time'].end()
        timerPrint(self.clock)

# %% Transfer and Update Functions

    def residualDispS(self):
        
        dispS = self.solverS.getDisplacement()
        self.residualS = dispS-self.interp.dispS

    # Transfers mechanical data fluid -> solid

    def transferLoadFS(self,com):

        if com.rank == 0: self.interp.getLoadF()
        self.interp.interpLoadFS(com)
        if com.rank == 1: self.interp.applyLoadS(self.step.nextTime)
        
    # Transfers mechanical data solid -> fluid

    def transferDispSF(self,com):
        
        self.interp.interpDispSF(com)
        if com.rank == 0: self.interp.applyDispF(self.step.dt)
