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
            self.maxDivision = 200

        else:
            
            self.implicit = True
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

# |-----------------------------------------|
# |   Run PFEM in the Current Time Frame    |
# |-----------------------------------------|
    
    @tb.write_logs
    @tb.compute_time
    def run(self):

        self.problem.setMaxSimTime(tb.Step.nexTime())
        self.problem.setMinTimeStep(tb.Step.dt/self.maxDivision)
        if self.implicit: self.solver.setTimeStep(tb.Step.dt)
        else: self.solver.computeNextDT()
        return self.problem.simulate()

# |------------------------------------|
# |   Dirichlet Boundary Conditions    |
# |------------------------------------|

    def applyDisplacement(self,disp):

        velocity = (disp-self.getPosition())/tb.Step.dt

        if self.implicit:
            for i in range(self.getSize()):
                self.BC[i][:self.dim] = velocity[i]

        else:
            acceler = (velocity-self.getVelocity())/(tb.Step.dt/2)

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

# |-----------------------------------------------|
# |   Backup and Reset the Boundary Conditions    |
# |-----------------------------------------------|

    def resetFSI(self):

        self.mesh.getNodesIndex('FSInterface',self.FSI)
        self.BC = list()

        for i in self.FSI:

            vector = w.VectorDouble(self.dim+1)
            self.mesh.getNode(i).setExtState(vector)
            self.BC.append(vector)

    @tb.compute_time
    def updateBackup(self):

        faceList = tb.Interp.sharePolytope()
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

    def wayBack(self):
        self.problem.loadSolution(self.prevSolution)

    @tb.write_logs
    @tb.compute_time
    def save(self): self.problem.dump()

    @tb.write_logs
    def exit(self): self.problem.displayTimeStats()
    def getSize(self): return self.FSI.size()

