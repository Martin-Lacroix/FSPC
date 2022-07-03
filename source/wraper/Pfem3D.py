import pfem3Dw as w
import numpy as np

# %% Initializes the Fluid Wraper

class Pfem3D(object):

    def __init__(self,param):

        path = param['inputF']
        self.read(path)

        # Problem class and functions initialization

        if self.ID == 'IncompNewtonNoT':

            self.run = self.runIncomp
            self.problem = w.ProbIncompNewton(path)
            self.applyDisplacement = self.applyDispIncomp

        elif self.ID == 'WCompNewtonNoT':

            self.run = self.runWcomp
            self.problem = w.ProbWCompNewton(path)
            self.applyDisplacement = self.applyDispWcomp

        else: raise Exception('Problem type not supported')

        # Stores the important objects and variables

        self.solver = self.problem.getSolver()
        self.prevSolution = w.SolutionData()
        self.mesh = self.problem.getMesh()
        self.dim = self.mesh.getDim()
        self.FSI = w.VectorInt()

        # FSI data and stores the previous time step 

        self.problem.copySolution(self.prevSolution)
        self.mesh.getNodesIndex(self.group,self.FSI)
        self.mesh.setComputeNormalCurvature(True)
        self.nbrNode = self.FSI.size()

        # Initializes the simulation data

        self.prevDisp = np.zeros((self.nbrNode,self.dim))
        self.disp = np.zeros((self.nbrNode,self.dim))

        # Initializes some FSPC data

        self.reload = False
        self.factor = 1
        self.ok = True
        self.div = 2

        # Prints the initial solution and stats

        self.problem.displayParams()
        self.problem.dump()

# %% Computes a Time Increment

    def runIncomp(self,t1,t2):

        if not (self.reload and self.ok): self.factor //= self.div
        self.factor = max(1,self.factor)
        self.reload = True
        iteration = 0

        # Main solving loop for the FSPC time step

        while iteration < self.factor:
            
            iteration += 1
            dt = (t2-t1)/self.factor
            self.solver.setTimeStep(dt)
            self.timeStats(dt+self.problem.getCurrentSimTime(),dt)
            self.ok = self.solver.solveOneTimeStep()

            if not self.ok:

                if self.div*self.factor > self.maxFactor: return False
                self.applyDisplacement(self.disp,t2-t1)
                self.factor *= self.div
                iteration = 0

        return True

    # For explicit weakly compressive flows

    def runWcomp(self,t1,t2):
        
        iteration = 0
        self.reload = True
        self.solver.computeNextDT()
        self.factor = int((t2-t1)/self.solver.getTimeStep())
        if self.factor > self.maxFactor: return False
        dt = (t2-t1)/self.factor
        self.timeStats(t2,dt)

        # Main solving loop for the FSPC time step

        while iteration < self.factor:
    
            iteration += 1
            self.solver.setTimeStep(dt)
            self.solver.solveOneTimeStep()

        return True

# %% Sets Boundary Conditions

    def applyDispIncomp(self,disp,dt):

        self.disp = disp.copy()
        if self.reload: self.problem.loadSolution(self.prevSolution)
        BC = (self.disp-self.prevDisp)/dt

        # Update the FSI node states BC

        for i in range(self.dim):
            for j in range(self.nbrNode):
                self.mesh.setNodeState(self.FSI[j],i,BC[j,i])

    # For explicit weakly compressive flows

    def applyDispWcomp(self,disp,dt):

        self.disp = disp.copy()
        if self.reload: self.problem.loadSolution(self.prevSolution)
        BC = 2*(disp-self.prevDisp-self.getVelocity()*dt)/(dt*dt)
        idx = int(self.dim+2)

        # Update the FSI node states BC

        for i in range(self.dim):
            for j in range(self.nbrNode):
                self.mesh.setNodeState(self.FSI[j],idx+i,BC[j,i])

# %% Gets Nodal Values

    def getPosition(self):

        pos = np.zeros((self.nbrNode,self.dim))

        for i in range(self.dim):
            for j in range(self.nbrNode):
                pos[j,i] = self.mesh.getNode(self.FSI[j]).getCoordinate(i)

        return pos

    # Computes the nodal velocity vector

    def getVelocity(self):

        vel = np.zeros((self.nbrNode,self.dim))

        for i in range(self.dim):
            for j in range(self.nbrNode):
                vel[j,i] = self.mesh.getNode(self.FSI[j]).getState(i)

        return vel
        
    # Computes the reaction nodal loads

    def getLoading(self):

        vec = w.VectorArrayDouble3()
        load = np.zeros((self.nbrNode,self.dim))
        self.solver.computeLoads(self.group,self.FSI,vec)
        for i in range(self.nbrNode): load[i] = vec[i][:self.dim]
        return -load

# %% Reads From the Lua File

    def read(self,path):

        file = open(path,'r')
        text = file.read().splitlines()
        file.close()

        for line in text:

            line = line.replace(' ','').replace('"','').replace("'",'')
            try: value = line.split('=')[1]
            except: continue

            if "Problem.id" in line: self.ID = value
            if "Problem.interface" in line: self.group = value
            if "Problem.maxFactor" in line: self.maxFactor = int(value)

# %% Other Functions

    def update(self):

        print('\nUpdate\n')
        self.mesh.remesh(False)
        if (self.ID == 'IncompNewtonNoT'): self.solver.precomputeMatrix()
        self.problem.copySolution(self.prevSolution)
        self.prevDisp = self.disp.copy()
        self.reload = False

    def timeStats(self,time,dt):

        start = self.problem.getCurrentSimTime()
        print('[PFEM-1] : t1 = {:.5e} - dt = {:.3e}'.format(start,dt))
        print('[PFEM-2] : t2 = {:.5e} - factor = {:.0f}'.format(time,self.factor))
        print('----------------------------')

    def save(self):
        self.problem.dump()

    def exit(self):
        self.problem.displayTimeStats()
        