from ..toolbox import write_logs,compute_time
import pfem3Dw as w
import numpy as np

# %% Initializes the Fluid Wraper

class Pfem3D(object):
    def __init__(self,path):

        mecha = w.getLuaBool(path,'Problem','mecha')
        thermo =  w.getLuaBool(path,'Problem','thermo')
        self.group = w.getLuaString(path,'Problem','interface')
        self.maxFactor = w.getLuaInt(path,'Problem','maxFactor')

        # Incompressible or weakly compressible solver

        self.problem = w.getProblem(path)
        problemType = self.problem.getID()
        if 'WC' in problemType: self.implicit = False
        else: self.implicit = True

        # Store the important objects and variables

        self.FSI = w.VectorInt()
        self.mesh = self.problem.getMesh()
        self.mesh.getNodesIndex(self.group,self.FSI)
        self.autoRemesh = self.problem.hasAutoRemeshing()
        self.solver = self.problem.getSolver()
        self.nbrNode = self.FSI.size()

        # Initialize the boundary conditions

        self.BC = list()
        self.dim = self.mesh.getDim()
        self.size = int(thermo)+int(self.dim*mecha)

        for i in self.FSI:

            vector = w.VectorDouble(self.size)
            self.mesh.getNode(i).setExtState(vector)
            self.BC.append(vector)

        # Save mesh after initializing the BC pointer

        self.prevSolution = w.SolutionData()
        self.problem.copySolution(self.prevSolution)
        self.problem.displayParams()

        # Store temporary simulation variables

        self.disp = np.zeros((self.nbrNode,self.dim))
        self.initPos = self.getPosition()
        self.vel = self.getVelocity()
        self.reload = False
        self.factor = 1
        self.ok = True

# %% Calculate One Time Step

    # To do : Not restart from (t1) if fail
    # To do : Try self.factor = 1 at every run
    # To do : Think about self.autoremeshing = true

    @write_logs
    @compute_time
    def run(self,t1,t2):
        
        print('\nt = {:.5e} - dt = {:.5e}'.format(t2,t2-t1))
        if self.implicit: return self.runImplicit(t1,t2)
        else: return self.runExplicit(t1,t2)

    # Run for implicit integration scheme

    def runImplicit(self,t1,t2):

        if not (self.reload and self.ok): self.factor //= 2
        self.factor = max(1,self.factor)
        self.resetSystem()

        # Main solving loop for the FSPC time step

        while self.iteration < self.factor:
            
            self.iteration += 1
            dt = (t2-t1)/self.factor
            self.solver.setTimeStep(dt)
            self.ok = self.solver.solveOneTimeStep()

            if not self.ok:

                if 2*self.factor > self.maxFactor: return False
                self.factor = 2*self.factor
                self.resetSystem()

        return True

    # Run for explicit integration scheme

    def runExplicit(self,t1,t2):
        
        self.resetSystem()
        self.solver.computeNextDT()
        self.factor = int((t2-t1)/self.solver.getTimeStep())
        if self.factor > self.maxFactor: return False
        dt = (t2-t1)/self.factor

        # Main solving loop for the FSPC time step

        while self.iteration < self.factor:
    
            self.iteration += 1
            self.solver.setTimeStep(dt)
            self.solver.solveOneTimeStep()

        return True

# %% Dirichlet Boundary Conditions

    def applyDisplacement(self,disp,dt):
        
        BC = (disp-self.disp)/dt
        if not self.implicit: BC = 2*(BC-self.vel)/dt

        for i,vector in enumerate(BC):
            for j,val in enumerate(vector): self.BC[i][j] = val

    # Update the Dirichlet nodal temperature

    def applyTemperature(self,temp):

        for i,vector in enumerate(temp):
            self.BC[i][self.size-1] = vector[0]
            
# %% Return Nodal Values

    def getPosition(self):

        vector = np.zeros(self.disp.shape)

        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                vector[j,i] = self.mesh.getNode(k).getCoordinate(i)

        return vector

    # Computes the nodal velocity vector

    def getVelocity(self):

        vector = np.zeros(self.disp.shape)
        
        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                vector[j,i] = self.mesh.getNode(k).getState(i)

        return vector
        
    # Mechanical boundary conditions

    @compute_time
    def getLoading(self):

        vector = w.VectorVectorDouble()
        self.solver.computeStress(self.group,self.FSI,vector)
        return np.copy(vector)

    # Thermal boundary conditions

    @compute_time
    def getHeatFlux(self):

        vector = w.VectorVectorDouble()
        self.solver.computeHeatFlux(self.group,self.FSI,vector)
        return np.copy(vector)

# %% Other Functions

    @compute_time
    def update(self):

        self.mesh.remesh(False)
        if self.implicit: self.solver.precomputeMatrix()
        self.problem.copySolution(self.prevSolution)
        self.disp = self.getPosition()-self.initPos
        self.vel = self.getVelocity()
        self.reload = False
    
    # Prepare to solve one time step

    def resetSystem(self):

        if self.reload: self.problem.loadSolution(self.prevSolution)
        if self.autoRemesh and self.implicit and self.reload:
            self.solver.precomputeMatrix()

        self.iteration = 0
        self.reload = True

    # Save the results or finalize

    @write_logs
    @compute_time
    def save(self): self.problem.dump()

    @write_logs
    def exit(self): self.problem.displayTimeStats()
        