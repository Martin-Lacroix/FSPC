from ..general import toolbox as tb
import pfem3Dw as w
import numpy as np

# Fluid solver wrapper class for PFEM3D

class Solver(object):
    def __init__(self, path: str):
        '''
        Initialize the fluid solver wrapper class
        '''

        import atexit
        atexit.register(self.print_clock)
        self.problem = w.getProblem(path)

        # Incompressible or weakly compressible solver

        if 'WC' in self.problem.getID():

            self.WC = True
            self.max_division = 1000

        else:

            self.WC = False
            self.max_division = 1

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

    @tb.write_logs
    @tb.compute_time
    def run(self):
        '''
        Run the fluid solver within the current time step
        '''

        self.problem.setMinTimeStep(tb.Step.dt/self.max_division)
        self.problem.setMaxSimTime(tb.Step.next_time())

        if self.WC: self.solver.computeNextDT()
        else: self.solver.setTimeStep(tb.Step.dt)
        return self.problem.simulate()

    def apply_displacement(self, disp: np.ndarray):
        '''
        Apply the displacement from the solid to the fluid interface
        '''

        BC = (disp-self.get_position())/tb.Step.dt
        if self.WC: BC = (BC-self.get_velocity())/(tb.Step.dt/2)

        for i, vector in enumerate(self.BC):
            for j, value in enumerate(BC[i]): vector[j] = value

    def apply_temperature(self, temp: np.ndarray):
        '''
        Apply the temperature from the solid to the fluid interface
        '''

        for i, vector in enumerate(self.BC):
            vector[self.dim] = temp[i][0]

    def get_loading(self):
        '''
        Return the nodal loading of the fluid interface
        '''

        vector = w.VectorVectorDouble()
        self.solver.computeStress('FSInterface', self.FSI, vector)
        return np.copy(vector)

    def get_heatflux(self):
        '''
        Return the nodal heat flux of the fluid interface
        '''

        vector = w.VectorVectorDouble()
        self.solver.computeHeatFlux('FSInterface', self.FSI, vector)
        return np.copy(vector)

    def get_position(self):
        '''
        Return the nodal positions of the fluid interface
        '''

        result = np.zeros((self.get_size(), self.dim))

        for i, data in enumerate(result):

            node = self.mesh.getNode(self.FSI[i])
            for j in range(self.dim): data[j] = node.getCoordinate(j)

        return result

    def get_velocity(self):
        '''
        Return the nodal velocity of the fluid interface
        '''

        result = np.zeros((self.get_size(), self.dim))

        for i, data in enumerate(result):

            node = self.mesh.getNode(self.FSI[i])
            for j in range(self.dim): data[j] = node.getState(j)

        return result

    def reset_interface_BC(self):
        '''
        Destroy and create the nodal exterior state container
        '''

        self.BC = list()
        self.mesh.getNodesIndex('FSInterface', self.FSI)

        for i in self.FSI:

            vector = w.VectorDouble(self.dim+1)
            self.mesh.getNode(i).setExtState(vector)
            self.BC.append(vector)

    def update_polytope(self, polytope: list):
        '''
        Update the polytope list using the solid boundary
        '''

        for i, face_list in enumerate(polytope):

            vec = w.VectorVectorDouble(face_list)
            try: self.mesh.updatePoly(self.poly[i], vec)
            except: self.poly.append(self.mesh.addPolytope(vec))

    @tb.compute_time
    def update(self, surface_mesh: list):
        '''
        Remesh and store the current state of the solver
        '''

        self.update_polytope(surface_mesh)
        self.mesh.remesh(verboseOutput = False)
        self.reset_interface_BC()

        # Update the backup and precompute matrices

        if not self.WC: self.solver.precomputeMatrix()
        self.problem.copySolution(self.prev_solution)

    @tb.compute_time
    def way_back(self):
        '''
        Revert back the solver to its last converged FSI state
        '''

        if self.problem.getCurrentSimStep() > self.prev_solution.step:
            self.problem.loadSolution(self.prev_solution)

    @tb.write_logs
    @tb.compute_time
    def save(self):
        '''
        Write the current fluid solution on the disk
        '''

        self.problem.dump()

    def get_size(self):
        '''
        Return the number of nodes on the fluid interface mesh
        '''

        return self.FSI.size()

    @tb.write_logs
    def print_clock(self):
        '''
        Print the computation times measured during the simulation
        '''

        self.problem.displayTimeStats()
