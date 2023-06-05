# <img src="Python.svg" width="60"/> Main Script

<br />

FSPC provides some classes able to perform FSI simulation by partitioned coupling of a fluid (PFEM) and a structural (Metafor) solver. This package uses MPI for the communication between them, and assumes that the solvers are available in your path. An example of how to run your Python script with FSPC is provided bellow.

<br />

```sh
    export OPTION="-map-by node:PE=${CPU_PER_PROC}"
    mpiexec ${OPTION} -n 2 python3 ${SCRIPT} -k ${CPU_PER_PROC}
```

| Input               | Type           | Description                                   |
|---------------------|----------------|-----------------------------------------------|
| *CPU_PER_PROC*      | *int*          | *number of CPU per MPI process*               |
| *SCRIPT*            | *string*       | *path to the Python script to be run*         |

<br />

The first step is to import the package and create the `Process` class. The latter initializes MPI for Python and provides a method to initialize the external solver wrappers with their respective input files. At that point, the script is run on two MPI processes. The returned `Solver` class corresponds to the fluid wrapper on the rank 0 and to the solid wrapper on the rank 1.

<br />

```python
    import FSPC                                 # Import the FSPC library
    process = FSPC.Process()                    # Initialize the MPI process
    solver = process.getSolver(pathF,pathS)     # Return the solver wrapper
    communicator = process.com                  # MPI world communication class
    rank = process.com.rank                     # Rank of the current process
```

| Input             | Type              | Description                                   |
|-------------------|-------------------|-----------------------------------------------|
| *pathF*           | *string*          | *input file path for the fluid solver*        |
| *pathS*           | *string*          | *input file path for the solid solver*        |

<br />

Different Algorithm classes are available in FSPC. The simplest one is the Block Gauss–Seidel `BGS` method, the two interface quasi-Newton methods are called Inverse Least Square `ILS` and Multi-Vector Jacobian `MVJ`. Each of them requires the solver previously obtained by the Process class.

<br />

```python
    algorithm = FSPC.BGS(solver)    # Block-Gauss Seidel with Aitken dynamic relexation
    algorithm = FSPC.ILS(solver)    # Interface quasi-Newton with inverse least squares 
    algorithm = FSPC.MVJ(solver)    # Interface quasi-Newton with multi-vector Jacobian
```

| Input             | Type                      | Description                               |
|-------------------|---------------------------|-------------------------------------------|
| *solver*          | *class*                   | *fluid or solid solver wrapper*           |

<br />

The convergence and the time step are managed by the `Convergence` and the `TimeStep` classes respectively. The latter should be given to the `Algorithm` as presented bellow. It is important to note that the type of coupling is enabled by the creation of the associated class such that `convergM` enables the mechanical coupling and `convergT` enables the thermal coupling.


<br />

```python
    algorithm.convergM = FSPC.Convergence(tol)      # Mechanical convergence class
    algorithm.convergT = FSPC.Convergence(tol)      # Thermal convergence class
    algorithm.step = FSPC.TimeStep(dt,dtSave)       # Time step manager class
```

| Input             | Type                      | Description                                |
|-------------------|---------------------------|--------------------------------------------|
| *tol*             | *float*                   | *tolerance for the FSI iterations*         |
| *dtSave*          | *float*                   | *time step for saving on the disk*         |
| *dt*              | *float*                   | *initial coupling time step*          |

<br />

The tolerance has the dimension of the Dirichlet condition exchanged between the solver, so a position for the mechanical coupling and a temperature for the thermal coupling. The initial time step is also the maximum allowed time step. Finally, additional variables must be initialized in order to run an FSI simulation.

<br />

```python
    algorithm.omega = omega             # Gauss Seidel relaxation parameter
    algorithm.maxIter = maxIter         # Maximum number of FSI iterations
    algorithm.endTime = endTime         # Final physical simulation time
```

| Input             | Type                      | Description                               |
|-------------------|---------------------------|-------------------------------------------|
| *omega*           | *float*                   | *initial relaxation parameter*            |
| *maxIter*         | *int*                     | *maximum number of FSI iterations*        |
| *endTime*         | *float*                   | *final simulation time*                   |

<br />

The `Interpolator` class manages the data transfer between the two interface meshes associated with the fluid and solid structure. The `KNN` uses a simple interpolation between the k nearest neighbour nodes in the target mesh. The `RBF` performs an interpolation based on user-defined radial basis functions. The `ETM` performs an orthogonal projection on the target mesh and uses the shape functions for the interpolation. If the fluid and solid meshes are matching at the interface, the k-nearest neighbours with `k = 1` is advised. For complex interface geometries, the `ETM` is the most robust algorithm.

<br />

```python
    algorithm.interp = FSPC.KNN(solver,k)           # K-nearest neighbours interpolator
    algorithm.interp = FSPC.RBF(solver,fun)         # Radial basis function interpolator
    algorithm.interp = FSPC.ETM(solver,nElem)       # Direct element transfer method
```

| Input             | Type                      | Description                                     |
|-------------------|---------------------------|-------------------------------------------------|
| *k*               | *int*                     | *number of nearest neighbours*                  |
| *fun*             | *function*                | *radial basis function for nodal distance*      |
| *nElem*           | *int*                     | *number of projection checking*                 |

<br />

Once the algorithm class has been initialized, the FSI simulation can be started with the `simulate` function provided by the `ALgorithm` class. The latter will fail if the parameters presented previously have not been correctly initialized. It is also possible to print the time stats at the end of the run and compare the computation time for the fluid and the solid parts.

<br />

```python
    algorithm.simulate()        # Run the FSI simulation
    FSPC.printClock()           # Print the final time stats
```

<br />

# <img src="Python.svg" width="60"/> PFEM3D File

<br />

The input file for the fluid solver is the standard Lua for [PFEM3D](https://github.com/ImperatorS79/PFEM3D). Because the time step and total simulation time are controlled by FSPC, the related variables in `Problem.Solver` are not used. It is also recommended setting the parameter `adaptDT` to `true` and disabling the automatic remeshing because FSPC is already performing a remeshing at the end of each coupling time step.

<br />

```lua
    Problem.autoRemeshing = false       -- Disable the automatic remeshing
    Problem.Solver.adaptDT = true       -- Enable adaptive time step
```

<br />

In order to enable the FSI coupling, it is mandatory to give the name `FSInterface` to the physical group representing your fluid-structure interface in Gmsh, and activate the external boundary conditions on this interface. This allows FSPC to dynamically enforce a Dirichlet condition on the nodes of this physical group.

<br />

```lua
    Problem.Mesh.mshFile = 'geometry.msh'                       -- Load the fluid mesh
    Problem.Solver.HeatEq.BC['FSInterfaceTExt'] = true          -- Enable thermal coupling
    Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true       -- Enable mechanical coupling
```

<br />

# <img src="Python.svg" width="60"/> Metafor File

<br />

Empty