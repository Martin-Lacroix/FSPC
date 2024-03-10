from ..general import toolbox as tb
import pfem3Dw as w
import numpy as np

# |-----------------------------------|
# |   Initializes the Fluid Wraper    |
# |-----------------------------------|

class PFEM3D(object):
    def __init__(self,path):

        self.problem = w.getProblem(path)

        # Incompressible or weakly compressible solver

        if 'WC' in self.problem.getID():
            
            self.implicit = False
            self.max_division = 200

        else:
            
            self.implicit = True
            self.max_division = 10

        # Store important classes and variables

        self.mesh = self.problem.getMesh()
        self.solver = self.problem.getSolver()
        self.dim = self.mesh.getDim()

        # Initialize the communication objects

        self.POLY = list()
        self.FSI = w.VectorInt()
        self.reset_interface_BC()

        # Save the current mesh for next way back

        self.prev_solution = w.SolutionData()
        self.problem.copySolution(self.prev_solution)
        self.problem.displayParams()

# |-----------------------------------------|
# |   Run PFEM in the Current Time Frame    |
# |-----------------------------------------|
    
    @tb.write_logs
    @tb.compute_time
    def run(self):

        self.problem.setMinTimeStep(tb.Step.dt/self.max_division)
        self.problem.setMaxSimTime(tb.Step.next_time())

        if self.implicit: self.solver.setTimeStep(tb.Step.dt)
        else: self.solver.computeNextDT()
        return self.problem.simulate()

# |------------------------------------|
# |   Dirichlet Boundary Conditions    |
# |------------------------------------|

    def apply_displacement(self,disp):

        velocity = (disp-self.get_position())/tb.Step.dt

        if self.implicit:
            for i in range(self.get_size()):
                self.BC[i][:self.dim] = velocity[i]

        else:
            acceler = (velocity-self.get_velocity())/(tb.Step.dt/2)

            for i in range(self.get_size()):
                self.BC[i][:self.dim] = acceler[i]

    # Update the Dirichlet nodal temperature

    def apply_temperature(self,temp):

        for i,result in enumerate(temp):
            self.BC[i][self.dim] = result[0]

# |----------------------------------|
# |   Neumann Boundary Conditions    |
# |----------------------------------|

    def get_loading(self):

        vector = w.VectorVectorDouble()
        self.solver.computeStress('FSInterface',self.FSI,vector)
        return np.copy(vector)

    # Return Thermal boundary conditions

    def get_heatflux(self):

        vector = w.VectorVectorDouble()
        self.solver.computeHeatFlux('FSInterface',self.FSI,vector)
        return np.copy(vector)

# |-----------------------------------|
# |   Return Position and Velocity    |
# |-----------------------------------|

    def get_position(self):

        result = np.zeros((self.get_size(),self.dim))

        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                result[j,i] = self.mesh.getNode(k).getCoordinate(i)

        return result

    # Computes the nodal velocity vector

    def get_velocity(self):

        result = np.zeros((self.get_size(),self.dim))
        
        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                result[j,i] = self.mesh.getNode(k).getState(i)

        return result

# |-------------------------------------------|
# |   Reset the FSI and Boundary Condition    |
# |-------------------------------------------|

    def reset_interface_BC(self):

        self.BC = list()
        self.mesh.getNodesIndex('FSInterface',self.FSI)

        for i in self.FSI:

            vector = w.VectorDouble(self.dim+1)
            self.mesh.getNode(i).setExtState(vector)
            self.BC.append(vector)

    # Create or update the exclusion boundary

    def update_polytope(self,polytope):

        for i,face_list in enumerate(polytope):
            
            vec = w.VectorVectorDouble(face_list)
            try: self.mesh.updatePoly(self.POLY[i],vec)
            except: self.POLY.append(self.mesh.addPolytope(vec))

# |------------------------------------------|
# |   Update the Solver After Convergence    |
# |------------------------------------------|

    @tb.compute_time
    def update(self,polytope):

        self.update_polytope(polytope)
        self.mesh.remesh(verboseOutput = False)
        self.reset_interface_BC()

        # Update the backup and precompute matrices

        if self.implicit: self.solver.precomputeMatrix()
        self.problem.copySolution(self.prev_solution)

# |------------------------------|
# |   Other Wrapper Functions    |
# |------------------------------|

    def way_back(self):
        self.problem.loadSolution(self.prev_solution)

    @tb.write_logs
    @tb.compute_time
    def save(self): self.problem.dump()

    @tb.write_logs
    def exit(self): self.problem.displayTimeStats()
    def get_size(self): return self.FSI.size()

