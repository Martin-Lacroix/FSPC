from ..general import Toolbox as tb
import pfem3Dw as w
import numpy as np

# |-----------------------------------|
# |   Initializes the Fluid Wraper    |
# |-----------------------------------|

class Pfem3D(object):
    def __init__(self,path):

        self.problem = w.getProblem(path)

        # Incompressible or weakly compressible solver

        if 'WC' in self.problem.getID():
            
            self.implicit = False
            self.run = getattr(self,'runExplicit')
            self.maxDivision = 200

        else:
            
            self.implicit = True
            self.run = getattr(self,'runImplicit')
            self.maxDivision = 10

        # Store important classes and variables

        self.FSI = w.VectorInt()
        self.mesh = self.problem.getMesh()
        self.solver = self.problem.getSolver()
        self.dim = self.mesh.getDim()

        # Initialize the communication objects

        self.resetFSI()
        vec = w.VectorVectorDouble()
        self.polyIdx = self.mesh.addPolytope(vec)

        # Save the current mesh for next way back

        self.prevSolution = w.SolutionData()
        self.problem.copySolution(self.prevSolution)
        self.problem.displayParams()

# |------------------------------------------|
# |   Run for Implicit Integration Scheme    |
# |------------------------------------------|

    @tb.write_logs
    @tb.compute_time
    def runImplicit(self):

        count = int(1)
        dt = tb.step.dt
        t2 = tb.step.nexTime()
        print('\nt = {:.5e} - dt = {:.5e}'.format(t2,dt))

        # Main solving loop for the fluid simulation

        while count > 0:
            
            self.solver.setTimeStep(dt)
            if not self.solver.solveOneTimeStep():
                
                dt = float(dt/2)
                count = np.multiply(2,count)
                if dt < tb.step.dt/self.maxDivision: return False
                continue

            count = count-1
        return True

# |------------------------------------------|
# |   Run for Explicit Integration Scheme    |
# |------------------------------------------|

    @tb.write_logs
    @tb.compute_time
    def runExplicit(self):

        iteration = 0
        dt = tb.step.dt
        t2 = tb.step.nexTime()
        print('\nt = {:.5e} - dt = {:.5e}'.format(t2,dt))

        # Estimate the time step for stability

        self.solver.computeNextDT()
        division = np.ceil(dt/self.solver.getTimeStep())
        if division > self.maxDivision: return False
        dt = dt/division

        # Main solving loop for the fluid simulation

        while iteration < division:
    
            iteration += 1
            self.solver.setTimeStep(dt)
            self.solver.solveOneTimeStep()

        return True

# |------------------------------------|
# |   Dirichlet Boundary Conditions    |
# |------------------------------------|

    def applyDisplacement(self,disp):

        velocity = (disp-self.getPosition())/tb.step.dt

        if self.implicit:
            for i in range(self.getSize()):
                self.BC[i][:self.dim] = velocity[i]

        else:
            acceler = (velocity-self.getVelocity())/(tb.step.dt/2)

            for i in range(self.getSize()):
                self.BC[i][:self.dim] = acceler[i]

    # Update the Dirichlet nodal temperature

    def applyTemperature(self,temp):

        for i,result in enumerate(temp):
            self.BC[i][self.dim] = result[0]

# |----------------------------------|
# |   Neumann Boundary Conditions    |
# |----------------------------------|

    @tb.compute_time
    def getLoading(self):

        vector = w.VectorVectorDouble()
        self.solver.computeStress('FSInterface',self.FSI,vector)
        return np.copy(vector)

    # Return Thermal boundary conditions

    @tb.compute_time
    def getHeatFlux(self):

        vector = w.VectorVectorDouble()
        self.solver.computeHeatFlux('FSInterface',self.FSI,vector)
        return np.copy(vector)

# |-----------------------------------|
# |   Return Position and Velocity    |
# |-----------------------------------|

    def getPosition(self):

        result = np.zeros((self.getSize(),self.dim))

        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                result[j,i] = self.mesh.getNode(k).getCoordinate(i)

        return result

    # Computes the nodal velocity vector

    def getVelocity(self):

        result = np.zeros((self.getSize(),self.dim))
        
        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                result[j,i] = self.mesh.getNode(k).getState(i)

        return result

# |---------------------------------------|
# |   Update the Communication Vectors    |
# |---------------------------------------|

    def resetFSI(self):

        self.mesh.getNodesIndex('FSInterface',self.FSI)
        self.BC = list()

        for i in self.FSI:

            vector = w.VectorDouble(self.dim+1)
            self.mesh.getNode(i).setExtState(vector)
            self.BC.append(vector)

    @tb.compute_time
    def update(self):

        faceList = tb.interp.sharePolytope()
        vector = w.VectorVectorDouble(faceList)
        self.mesh.updatePoly(self.polyIdx,vector)
        self.mesh.remesh(False)
        self.resetFSI()

        # Update the backup and precompute global matrices
        
        if self.implicit: self.solver.precomputeMatrix()
        self.problem.copySolution(self.prevSolution)

# |------------------------------|
# |   Other Wrapper Functions    |
# |------------------------------|

    @tb.compute_time
    def wayBack(self):
        self.problem.loadSolution(self.prevSolution)

    @tb.write_logs
    @tb.compute_time
    def save(self): self.problem.dump()

    @tb.write_logs
    def exit(self): self.problem.displayTimeStats()
    def getSize(self): return self.FSI.size()

