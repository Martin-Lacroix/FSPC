import pfem3Dw as w
import numpy as np

# %% Read Data From the Lua File

def read(path):

    with open(path,'r') as file: text = file.read()
    text = text.replace('"','').replace("'",'').replace(' ','')
    text = [x.split('=') for x in text.splitlines() if '=' in x]
    return dict(text)

# %% Initializes the Fluid Wraper

class Pfem3D(object):
    def __init__(self,param):

        path = param['inputF']
        input = read(path)

        # Read data from the lua file

        self.ID = input['Problem.id']
        self.group = input['Problem.interface']
        self.maxFactor = int(input['Problem.maxFactor'])
        self.autoRemesh = (input['Problem.autoRemeshing'] == 'true')

        # Problem class and functions initialization

        if self.ID == 'IncompNewtonNoT':

            self.run = self.runIncomp
            self.problem = w.ProbIncompNewton(path)
            self.applyDispBC = self.applyDispIncomp

        elif self.ID == 'WCompNewtonNoT':

            self.run = self.runWcomp
            self.problem = w.ProbWCompNewton(path)
            self.applyDispBC = self.applyDispWcomp

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
        self.problem.displayParams()
        self.nbrNode = self.FSI.size()

        # Initializes the simulation data

        self.disp = np.zeros((self.nbrNode,self.dim))
        self.initPos =  self.getPosition()
        self.reload = False
        self.factor = 1
        self.ok = True

# %% Run for Incompressible Flows

    def runIncomp(self,t1,t2):

        print('\nSolve ({:.5e}, {:.5e})'.format(t1,t2))
        print('----------------------------------')

        # The line order is important here

        if not (self.reload and self.ok): self.factor //= 2
        self.factor = max(1,self.factor)
        self.resetSystem(t2-t1)
        iteration = 0

        # Main solving loop for the FSPC time step

        while iteration < self.factor:
            
            iteration += 1
            dt = (t2-t1)/self.factor
            self.solver.setTimeStep(dt)
            self.timeStats(dt+self.problem.getCurrentSimTime(),dt)
            self.ok = self.solver.solveOneTimeStep()

            if not self.ok:

                print('PFEM3D: Problem occured\n')
                if 2*self.factor > self.maxFactor: return False
                self.factor = 2*self.factor
                self.resetSystem(t2-t1)
                iteration = 0

        print('PFEM3D: Successful run')
        return True

# %% Run for Weakly Compressible Flows

    def runWcomp(self,t1,t2):

        print('\nSolve ({:.5e}, {:.5e})'.format(t1,t2))
        print('----------------------------------')

        # Estimate the time step only once
        
        self.resetSystem(t2-t1)
        self.solver.computeNextDT()
        self.factor = int((t2-t1)/self.solver.getTimeStep())
        if self.factor > self.maxFactor: return False
        dt = (t2-t1)/self.factor
        self.timeStats(t2,dt)
        iteration = 0

        # Main solving loop for the FSPC time step

        while iteration < self.factor:
    
            iteration += 1
            self.solver.setTimeStep(dt)
            self.solver.solveOneTimeStep()

        print('PFEM3D: Successful run')
        return True

# %% Apply Boundary Conditions

    def applyDisplacement(self,disp):
        self.disp = disp.copy()

    # For implicit and incompressible flows

    def applyDispIncomp(self,distance,dt):

        BC = (distance)/dt
        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                self.mesh.setNodeState(k,i,BC[j,i])

    # For explicit weakly compressive flows

    def applyDispWcomp(self,distance,dt):

        velocity = self.getVelocity()
        BC = 2*(distance-velocity*dt)/(dt*dt)

        # Update the FSI node states BC

        for i in range(self.dim):
            idx = int(self.dim+2+i)

            for j,k in enumerate(self.FSI):
                self.mesh.setNodeState(k,idx,BC[j,i])

# %% Return Nodal Values

    def getPosition(self):

        pos = self.disp.copy()
        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                pos[j,i] = self.mesh.getNode(k).getCoordinate(i)

        return pos

    # Computes the nodal velocity vector

    def getVelocity(self):

        vel = self.disp.copy()
        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                vel[j,i] = self.mesh.getNode(k).getState(i)

        return vel
        
    # Computes the reaction nodal loads

    def getLoading(self):

        vec = w.VectorArrayDouble3()
        load = np.zeros((self.nbrNode,self.dim))
        self.solver.computeLoads(self.group,self.FSI,vec)
        for i,array in enumerate(vec): load[i] = array[:self.dim]
        return -load

# %% Other Functions

    def update(self):

        self.mesh.remesh(False)
        if (self.ID == 'IncompNewtonNoT'): self.solver.precomputeMatrix()
        self.problem.copySolution(self.prevSolution)
        self.reload = False
    
    # Prepare to solve one time step

    def resetSystem(self,dt):

        if self.reload: self.problem.loadSolution(self.prevSolution)
        if self.autoRemesh and (self.ID == 'IncompNewtonNoT'):
            if self.reload: self.solver.precomputeMatrix()

        distance = self.disp-(self.getPosition()-self.initPos)
        self.applyDispBC(distance,dt)
        self.reload = True

    # Display the current simulation state

    def timeStats(self,time,dt):

        start = self.problem.getCurrentSimTime()
        print('t1 = {:.5e} - dt = {:.3e}'.format(start,dt))
        print('t2 = {:.5e} - factor = {:.0f}'.format(time,self.factor))
        print('----------------------------------')

    # Save the results or finalize

    def save(self):
        self.problem.dump()

    def exit(self):
        self.problem.displayTimeStats()
        