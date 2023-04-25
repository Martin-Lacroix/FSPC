# <img src="Python.svg" width="60"/> Initialization

<br />

FSPC provides some classes able to perform FSI simulation by partitioned coupling of a fluid and a structural solver. Currently, only PFEM3D and the Metafor solvers are supported. Moreover, FSPC uses MPI for the communication between the two solvers, each of them relying on a single process. FSPC assumes that the solvers are available in your path.

```python
    import FSPC                                     # Import the FSPC library
    process = FSPC.Process()                        # Initialize the MPI process
    solver = process.getSolver(pathF,pathS)         # Return the solver wrapper
```

| Input             | Type              | Description                                   |
|-------------------|-------------------|-----------------------------------------------|
| *pathF*           | *string*          | *input file path for the fluid solver*        |
| *pathS*           | *string*          | *input file path for the solid solver*        |

<br />

The solver variable is the fluid wrapper on the rank 0 and the solid wrapper on the rank 1. This rank as well as the MPI communicators can be obtained by:

```python
    communicator = process.com      # MPI world communication class
    rank = process.com.rank         # Rank of the current process
```

<br />

# <img src="Python.svg" width="60"/> Algorithm Class

<br />


Different algorithm classes are available in FSPC. Each of them require the solver previously obtained by the process class:

```python
    algorithm = FSPC.BGS(solver)        # Block-Gauss Seidel with Aitken dynamic relexation
    algorithm = FSPC.ILS(solver)        # Interface quasi-Newton with inverse least squares 
    algorithm = FSPC.MVJ(solver)        # Interface quasi-Newton with multi-vector Jacobian
```

| Input             | Type                      | Description                               |
|-------------------|---------------------------|-------------------------------------------|
| *solver*          | *class*                   | *fluid or solid solver wrapper*           |

<br />

The convergence and the time step are managed by individual classes. The type of coupling is defined by the presence of the associated class such that `convergM` enables mechanical coupling and `convergT` enables thermal coupling.

```python
    algorithm.convergM = FSPC.Convergence(tol)      # Mechanical convergence class
    algorithm.convergT = FSPC.Convergence(tol)      # Thermal convergence class
    algorithm.step = FSPC.TimeStep(dt,dtSave)       # Time step manager class
```

| Input             | Type                      | Description                                |
|-------------------|---------------------------|--------------------------------------------|
| *tol*             | *float*                   | *tolerance for the FSI iterations*         |
| *dtSave*          | *float*                   | *time step for saving on the disk*         |
| *dt*              | *float*                   | *initial time coupling time step*          |

<br />

Additional variables must be initialized in order to run an FSI simulation:

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

# <img src="Python.svg" width="60"/> Interpolator Class

<br />

The interpolator manages the data transfer between the two solvers. If the fluid and solid meshes are matching at the interface, the k-nearest neighbours with `k = 1` is advised.

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

# <img src="Python.svg" width="60"/> Simulation Run

<br />

Once the algorithm class has been initialized, the FSI simulation can be started with the `simulate` function. It is also possible to print the time stats at the end:

```python
    algorithm.simulate()        # Run the FSI simulation
    FSPC.printClock()           # Print the final time stats
```