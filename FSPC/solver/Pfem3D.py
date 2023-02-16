from ..toolbox import write_logs,compute_time
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
    def __init__(self,path):

        self.problem = w.getProblem(path)
        self.autoRemesh = self.problem.hasAutoRemeshing()
        problemID = self.problem.getID()

        # Read the input Lua file

        input = read(path)
        self.group = input['Problem.interface']
        self.maxFactor = int(input['Problem.maxFactor'])

        # Stores the important objects and variables

        self.solver = self.problem.getSolver()
        self.prevSolution = w.SolutionData()
        self.mesh = self.problem.getMesh()
        self.dim = self.mesh.getDim()
        self.FSI = w.VectorInt()

        # We must add a getter in PFEM3D for this !!!

        if problemID[:2] == 'WC':

            self.implicit = False
            self.indexT = int(2*self.dim+2)
            self.indexM = int(self.dim+2)

        elif problemID == 'Conduction':

            self.implicit = True
            self.indexT = int(0)

        else:
            
            self.implicit = True
            self.indexT = int(self.dim+1)
            self.indexM = int(0)
            
        # FSI data and stores the previous time step 

        self.problem.copySolution(self.prevSolution)
        self.mesh.getNodesIndex(self.group,self.FSI)
        self.nbrNode = self.FSI.size()
        self.problem.displayParams()

        # Initializes the simulation data

        self.disp = np.zeros((self.nbrNode,self.dim))
        self.initPos =  self.getPosition()
        self.reload = False
        self.thermo = False
        self.mecha = False
        self.factor = 1
        self.ok = True

# %% Calculates One Time Step

    @write_logs
    @compute_time
    def run(self,t1,t2):

        print('\nSolve ({:.5e}, {:.5e})'.format(t1,t2))
        print('----------------------------------')
        if self.implicit: return self.runImplicit(t1,t2)
        else: return self.runExplicit(t1,t2)

    # Run for implicit integration scheme

    def runImplicit(self,t1,t2):

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

        return True

    # Run for explicit integration scheme

    def runExplicit(self,t1,t2):
        
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

        return True

# %% Dirichlet Boundary Conditions

    def applyDisplacement(self,disp):
        
        self.disp = np.copy(disp)
        self.mecha = True

    def applyTemperature(self,temp):
        
        self.temp = np.copy(temp)
        self.thermo = True

    # Update and apply the nodal displacement

    def applyDispBC(self,distance,dt):

        velocity = self.getVelocity()
        if self.implicit: BC = (distance)/dt
        else: BC = 2*(distance-velocity*dt)/(dt*dt)

        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                self.mesh.setNodeState(k,self.indexM+i,BC[j,i])

    # Update and apply the nodal temperatures

    def applyTempBC(self,temp):

        for i,k in enumerate(self.FSI):
            self.mesh.setNodeState(k,self.indexT,temp[i,0])
            
# %% Return Nodal Values

    def getPosition(self):

        vector = np.zeros((self.nbrNode,self.dim))

        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                vector[j,i] = self.mesh.getNode(k).getCoordinate(i)

        return vector

    # Computes the nodal velocity vector

    def getVelocity(self):

        vector = np.zeros((self.nbrNode,self.dim))
        
        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                vector[j,i] = self.mesh.getNode(k).getState(i)

        return vector
        
    # Mechanical boundary conditions

    @compute_time
    def getLoading(self):

        vector = w.VectorVectorDouble()
        self.solver.computeStress(self.group,self.FSI,vector)
        load = np.copy(vector)
        return load

    # Thermal boundary conditions

    @compute_time
    def getHeatFlux(self):

        vector = w.VectorVectorDouble()
        self.solver.computeHeatFlux(self.group,self.FSI,vector)
        heat = np.copy(vector)
        return heat

# %% Other Functions

    @compute_time
    def update(self):

        self.mesh.remesh(False)
        if self.implicit: self.solver.precomputeMatrix()
        self.problem.copySolution(self.prevSolution)
        self.reload = False
    
    # Prepare to solve one time step

    def resetSystem(self,dt):

        if self.reload: self.problem.loadSolution(self.prevSolution)
        if self.autoRemesh and self.implicit and self.reload:
            self.solver.precomputeMatrix()

        distance = self.disp-(self.getPosition()-self.initPos)
        if self.mecha: self.applyDispBC(distance,dt)
        if self.thermo: self.applyTempBC(self.temp)
        self.reload = True

    # Display the current simulation state

    def timeStats(self,time,dt):

        start = self.problem.getCurrentSimTime()
        print('t1 = {:.5e} - dt = {:.3e}'.format(start,dt))
        print('t2 = {:.5e} - factor = {:.0f}'.format(time,self.factor))
        print('----------------------------------')

    # Save the results or finalize

    @write_logs
    @compute_time
    def save(self): self.problem.dump()

    @write_logs
    def exit(self): self.problem.displayTimeStats()
        