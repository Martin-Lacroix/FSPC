from ..general import toolbox as tb
import pfem3Dw as w
import numpy as np

# Fluid solver wrapper class for PFEM3D

class Solver(tb.Static):
    def __init__(self, path: str):
        '''
        Initialize the fluid solver wrapper class
        '''

        # Load PFEM3D and defines a function called at exit

        import atexit
        atexit.register(self.print_clock)
        object.__setattr__(self, 'problem', w.getProblem(path))

        # Parameters for the explicit weakly compressible solver

        if 'WC' in self.problem.getID():

            object.__setattr__(self, 'WC', True)
            object.__setattr__(self, 'max_division', 1000)

        # Parameters for the implicit incompressible solver

        else:

            object.__setattr__(self, 'WC', False)
            object.__setattr__(self, 'max_division', 1)

        # Store the dimension and the interface nodes list

        object.__setattr__(self, 'dim', self.problem.getMesh().getDim())
        object.__setattr__(self, 'FSI', w.VectorInt())

        # Initialize the list of boundary conditions vectors

        object.__setattr__(self, 'BC', list())
        self.reset_interface_BC()

        # Save the current mesh solution and print the parameters

        object.__setattr__(self, 'prev_solution', w.SolutionData())
        self.problem.copySolution(self.prev_solution)
        self.problem.displayParams()

    @tb.write_logs
    @tb.compute_time
    def run(self):
        '''
        Run the fluid solver within the current time step
        '''

        # The minimal time step is set by the maximum division factor

        min_dt = tb.Step.dt/self.max_division
        self.problem.setMinTimeStep(min_dt)

        # Set the final time for the current FSI time step
        
        end = tb.Step.time+tb.Step.dt
        self.problem.setMaxSimTime(end)

        # Compute the time step in explicit or impose it in implicit

        if self.WC: self.problem.getSolver().computeNextDT()
        else: self.problem.getSolver().setTimeStep(tb.Step.dt)

        # Return true if PFEM3D solved the time step successfully

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

        # The temperature is stored at the last index of the BC vectors

        for i, vector in enumerate(self.BC):
            vector[self.dim] = temp[i][0]

    def get_loading(self):
        '''
        Return the nodal loading of the fluid interface
        '''

        vector = w.VectorVectorDouble()

        # This command will also update the node indices in FSI

        self.problem.getSolver().computeStress('FSInterface', self.FSI, vector)
        return np.copy(vector)

    def get_heatflux(self):
        '''
        Return the nodal heat flux of the fluid interface
        '''

        vector = w.VectorVectorDouble()

        # This command will also update the node indices in FSI

        self.problem.getSolver().computeHeatFlux('FSInterface', self.FSI, vector)
        return np.copy(vector)

    def get_position(self):
        '''
        Return the nodal positions of the fluid interface
        '''

        result = np.zeros((self.get_size(), self.dim))

        # Loop on the number of nodes in the fluid structure interface

        for i, data in enumerate(result):

            # Get the node index in PFEM3D and store the positions

            node = self.problem.getMesh().getNode(self.FSI[i])
            for j in range(self.dim): data[j] = node.getCoordinate(j)

        return result

    def get_velocity(self):
        '''
        Return the nodal velocity of the fluid interface
        '''

        result = np.zeros((self.get_size(), self.dim))

        # Loop on the number of nodes in the fluid structure interface

        for i, data in enumerate(result):

            # Get the node index in PFEM3D and store the velocities

            node = self.problem.getMesh().getNode(self.FSI[i])
            for j in range(self.dim): data[j] = node.getState(j)

        return result

    def reset_interface_BC(self):
        '''
        Destroy and create the nodal exterior state container
        '''

        # Clear the list of BC and update the interface node indices

        self.BC.clear()
        self.problem.getMesh().getNodesIndex('FSInterface', self.FSI)

        # Loop on the interface node indices

        for i in self.FSI:

            vector = w.VectorDouble(self.dim+1)

            # Store the vector of BC and send its pointer to PFEM3D

            self.problem.getMesh().getNode(i).setExtState(vector)
            self.BC.append(vector)

    @tb.compute_time
    def update(self):
        '''
        Remesh and store the current state of the solver
        '''

        # Perform a silent remeshing and reset the boundary conditions

        self.problem.getMesh().remesh(verboseOutput = False)
        self.reset_interface_BC()

        # Update the global matrix pattern if implicit solver

        if not self.WC: self.problem.getSolver().precomputeMatrix()

        # Save the current solution into a structure

        self.problem.copySolution(self.prev_solution)

    @tb.compute_time
    def way_back(self):
        '''
        Revert back the solver to its last converged FSI state
        '''

        # Check if the current step is above the last saved step

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
