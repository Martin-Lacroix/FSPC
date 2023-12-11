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

        # Store the important objects and variables

        self.FSI = w.VectorInt()
        self.mesh = self.problem.getMesh()
        self.solver = self.problem.getSolver()
        self.prevSolution = w.SolutionData()
        self.dim = self.mesh.getDim()

        # Initialize the polytope and display parameters

        vec = w.VectorVectorDouble()
        self.polyIdx = self.mesh.addPolytope(vec)
        self.problem.displayParams()

# |------------------------------------------|
# |   Run for Implicit Integration Scheme    |
# |------------------------------------------|

    @tb.write_logs
    @tb.compute_time
    def runImplicit(self):

        dt = tb.step.dt
        t2 = tb.step.nexTime()
        print('\nt = {:.5e} - dt = {:.5e}'.format(t2,dt))

        self.problem.loadSolution(self.prevSolution)
        count = int(1)

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

        dt = tb.step.dt
        t2 = tb.step.nexTime()
        print('\nt = {:.5e} - dt = {:.5e}'.format(t2,dt))

        self.problem.loadSolution(self.prevSolution)
        iteration = 0

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

        BC = disp/tb.step.dt
        if not self.implicit:
            BC = np.multiply(2,BC-self.vel)/tb.step.dt

        for i,vector in enumerate(BC):
            for j,val in enumerate(vector): self.BC[i][j] = val

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

# |--------------------------|
# |   Return Nodal Values    |
# |--------------------------|

    def getDisplacement(self):
        return self.getPosition()-self.prevPos
    
    # Computes the nodal position vector

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

# |---------------------------------------------|
# |   Remesh and Update the Internal Vectors    |
# |---------------------------------------------|

    @tb.compute_time
    def update(self):

        faceList = tb.interp.sharePolytope()
        vector = w.VectorVectorDouble(faceList)
        self.mesh.updatePoly(self.polyIdx,vector)
        self.mesh.remesh(False)

        # Update the interface and BC after remeshing

        self.mesh.getNodesIndex('FSInterface',self.FSI)
        self.BC = list()

        for i in self.FSI:

            vector = w.VectorDouble(self.dim+1)
            self.mesh.getNode(i).setExtState(vector)
            self.BC.append(vector)

        # Update data and precompute PFEM matrices

        if self.implicit: self.solver.precomputeMatrix()
        self.problem.copySolution(self.prevSolution)
        self.prevPos = self.getPosition()
        self.vel = self.getVelocity()

# |------------------------------|
# |   Other Wrapper Functions    |
# |------------------------------|

    @tb.write_logs
    @tb.compute_time
    def save(self): self.problem.dump()

    @tb.write_logs
    def exit(self): self.problem.displayTimeStats()
    def getSize(self): return self.FSI.size()
