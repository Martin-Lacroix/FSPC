from ..general import toolbox as tb
import pfem3Dw as w
import numpy as np

# |--------------------------------------|
# |   Fluid Solver Wrapper for PFEM3D    |
# |--------------------------------------|

class PFEM3D(object):
    def __init__(self, path: str):

        self.problem = w.getProblem(path)

        # Incompressible or weakly compressible solver

        if 'WC' in self.problem.getID():

            self.WC = True
            self.max_division = 1000

        else:

            self.WC = False
            self.max_division = 10

        # Store important classes and variables

        self.mesh = self.problem.getMesh()
        self.solver = self.problem.getSolver()
        self.dim = self.mesh.getDim()

        # Initialize the communication objects

        self.poly = list()
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

        if self.WC: self.solver.computeNextDT()
        else: self.solver.setTimeStep(tb.Step.dt)
        return self.problem.simulate()

# |----------------------------------------|
# |   Get Dirichlet Boundary Conditions    |
# |----------------------------------------|

    def apply_displacement(self, disp: np.ndarray):

        BC = (disp-self.get_position())/tb.Step.dt
        if self.WC: BC = (BC-self.get_velocity())/(tb.Step.dt/2)

        for i, vector in enumerate(self.BC):
            for j, value in enumerate(BC[i]): vector[j] = value

    # Update the Dirichlet nodal temperature

    def apply_temperature(self, temp: np.ndarray):

        for i, vector in enumerate(self.BC):
            vector[self.dim] = temp[i][0]

# |--------------------------------------|
# |   Get Neumann Boundary Conditions    |
# |--------------------------------------|

    def get_loading(self):

        vector = w.VectorVectorDouble()
        self.solver.computeStress('FSInterface', self.FSI, vector)
        return np.copy(vector)

    # Return Thermal boundary conditions

    def get_heatflux(self):

        vector = w.VectorVectorDouble()
        self.solver.computeHeatFlux('FSInterface', self.FSI, vector)
        return np.copy(vector)

# |-----------------------------------|
# |   Return Position and Velocity    |
# |-----------------------------------|

    def get_position(self):

        result = np.zeros((self.get_size(), self.dim))

        for i, data in enumerate(result):

            node = self.mesh.getNode(self.FSI[i])
            for j in range(self.dim): data[j] = node.getCoordinate(j)

        return result

    # Computes the nodal velocity vector

    def get_velocity(self):

        result = np.zeros((self.get_size(), self.dim))

        for i, data in enumerate(result):

            node = self.mesh.getNode(self.FSI[i])
            for j in range(self.dim): data[j] = node.getState(j)

        return result

# |-------------------------------------------|
# |   Reset the FSI and Boundary Condition    |
# |-------------------------------------------|

    def reset_interface_BC(self):

        self.BC = list()
        self.mesh.getNodesIndex('FSInterface', self.FSI)

        for i in self.FSI:

            vector = w.VectorDouble(self.dim+1)
            self.mesh.getNode(i).setExtState(vector)
            self.BC.append(vector)

    # Create or update the exclusion boundary

    def update_polytope(self, polytope: list):

        for i, face_list in enumerate(polytope):

            vec = w.VectorVectorDouble(face_list)
            try: self.mesh.updatePoly(self.poly[i], vec)
            except: self.poly.append(self.mesh.addPolytope(vec))

# |------------------------------------|
# |   Other Miscellaneous Functions    |
# |------------------------------------|

    @tb.compute_time
    def update(self, surface_mesh: list):

        self.update_polytope(surface_mesh)
        self.mesh.remesh(verboseOutput = False)
        self.reset_interface_BC()

        # Update the backup and precompute matrices

        if not self.WC: self.solver.precomputeMatrix()
        self.problem.copySolution(self.prev_solution)

    # Backup the solver state if needed

    @tb.compute_time
    def way_back(self):

        if self.problem.getCurrentSimStep() > self.prev_solution.step:
            self.problem.loadSolution(self.prev_solution)

    # Export the current solution into a file

    @tb.write_logs
    @tb.compute_time
    def save(self): self.problem.dump()

    # Return the number of nodes at the interface

    def get_size(self): return self.FSI.size()

    # Print the time stats at destruction

    def __del__(self): self.problem.displayTimeStats()

# |----------------------------------|
# |   2D Rupture Interface Update    |
# |----------------------------------|

    @tb.compute_time
    def check_rupture(self, recv_pos: np.ndarray):

        epsilon = 1e-6
        position = self.get_position()
        p_ext = self.solver.getPExt()

        tags = w.VectorInt(1)
        for i, tag in enumerate(self.mesh.getTagNames()):
            if(tag == "FSInterface"): tags[0] = i

        # Remove broken nodes from the FS interface

        for i, pos in enumerate(position):

            dist = np.linalg.norm(pos-recv_pos, axis=1)
            node = self.mesh.getNode(self.FSI[i])

            if(np.min(dist) > epsilon):

                if(node.isFree()):
                    self.mesh.nextRemove.push_back(self.FSI[i])

                else:
                    node.m_isOnFreeSurface = True
                    node.m_isBound = False
                    node.m_tags.clear()

        # Add new solid nodes on the FS interface

        for i, pos in enumerate(recv_pos):

            dist = np.linalg.norm(pos-position, axis=1)
            vector_pos = w.ArrayDouble3()
            states = w.VectorDouble(3)

            vector_pos[0] = pos[0]
            vector_pos[1] = pos[1]
            vector_pos[2] = 0

            states[0] = 0
            states[1] = 0
            states[2] = p_ext

            if(np.min(dist) > epsilon):
                self.mesh.addBoundaryNode(vector_pos, states, tags)