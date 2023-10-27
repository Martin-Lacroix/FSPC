# <img src="Python.svg" width="60"/> Main Script

<br />

FSPC provides some classes able to perform FSI simulation by partitioned coupling of a fluid (PFEM) and a structural (Metafor) solver. This package uses MPI for the communication between them, and assumes that the solvers are available in your path. An example of how to run your Python script with FSPC is provided bellow.

<br />

```sh
export OPTION="-map-by node:PE=${CPU_PER_PROC}"
mpiexec ${OPTION} -n 2 python ${SCRIPT} -k ${CPU_PER_PROC}
```

| Input               | Type           | Description                                   |
|---------------------|----------------|-----------------------------------------------|
| *CPU_PER_PROC*      | *int*          | *number of CPU per MPI process*               |
| *SCRIPT*            | *string*       | *path to the Python script to be run*         |

<br />

The first step is to import the package. The latter initializes MPI for Python and provides a method to initialize the external solver wrappers with their respective input files. At that point, the script is run on two MPI processes. One may then initialize some internal classes.

<br />

```python
import FSPC                         # Import the FSPC package
FSPC.setStep(dt,dtSave)             # Initialize the time step manager
FSPC.setSolver(pathF,pathS)         # Initialize the external solvers
```

| Input             | Type              | Description                                   |
|-------------------|-------------------|-----------------------------------------------|
| *dt*              | *float*           | *initial coupling time step*                  |
| *dtSave*          | *float*           | *time step for saving on the disk*            |
| *pathF*           | *string*          | *input file path for the fluid solver*        |
| *pathS*           | *string*          | *input file path for the solid solver*        |

<br />

The convergence criterion is managed by the `Convergence` class. The latter should be specified both for the displacement and the temperature when relevant. It is important to note that the type of coupling is enabled by the initialization of the associated class such that `setConvMech` enables the mechanical coupling and `setConvTher` enables the thermal coupling.

<br />

```python
FSPC.setConvMech(tolDisp)       # Mechanical convergence criterion
FSPC.setConvTher(tolTemp)       # Thermal convergence criterion
```

| Input             | Type              | Description                                |
|-------------------|-------------------|--------------------------------------------|
| *tolDisp*         | *float*           | *tolerance for the displacement FSI*       |
| *tolTemp*         | *float*           | *tolerance for the temperature FSI*        |

<br />

The tolerance is a relative change in the Dirichlet condition exchanged between the solver, so the position for the mechanical coupling and the temperature for the thermal coupling. The `Interpolator` class manages the data transfer between the two interface meshes associated with the fluid and solid structure. The `KNN` uses a simple interpolation between the k nearest neighbour nodes in the target mesh. The `RBF` performs an interpolation based on user-defined radial basis functions. The `ETM` performs an orthogonal projection on the target mesh and uses the shape functions for the interpolation. 

<br />

```python
FSPC.setInterp(FSPC.interpolator.KNN,k)           # K-nearest neighbours interpolator
FSPC.setInterp(FSPC.interpolator.RBF,fun)         # Radial basis function interpolator
FSPC.setInterp(FSPC.interpolator.ETM,nElem)       # Direct element transfer method
```

| Input             | Type                | Description                                     |
|-------------------|---------------------|-------------------------------------------------|
| *k*               | *int*               | *number of nearest neighbours*                  |
| *fun*             | *function*          | *radial basis function for nodal distance*      |
| *nElem*           | *int*               | *number of projection checking*                 |

<br />

Note that there is no required ordering when initializing the classes and the interpolator may be initialized before the `Convergence` class. Finally, the last step is the initialization of the`Algorithm` class. The simplest one is the block Gauss–Seidel `BGS` method. Moreover, two interface quasi-Newton methods are available, with inverse least square `ILS` and multi-vector Jacobian `MVJ` respectively.

<br />

```python
FSPC.setAlgo(FSPC.algorithm.BGS,maxIter)        # Aitken Block-Gauss Seidel
FSPC.setAlgo(FSPC.algorithm.ILS,maxIter)        # IQN with inverse least squares 
FSPC.setAlgo(FSPC.algorithm.MVJ,maxIter)        # IQN with multi-vector Jacobian
```

| Input             | Type                | Description                                     |
|-------------------|---------------------|-------------------------------------------------|
| *maxIter*         | *int*               | *maximum number of iterations*                  |

<br />

It is important to note that each `Set` function returns a reference to the class created. Thereby, some additional parameters such as the initial Aitken relaxation factor can be modified by the user. This is achieved by assigning a new value to the corresponding attribute, for instance `algorithm.omega = 0.5` is the default Aitken parameter. The simulation can be started with the `simulate` function provided by the `general` module. It is also possible to print the time stats at the end of the simulation and compare the computation time for the fluid and the solid processes.

<br />

```python
FSPC.general.simulate(endTime)      # Run the FSI simulation
FSPC.general.printClock()           # Print the final time stats
```

| Input             | Type              | Description                                  |
|-------------------|-------------------|----------------------------------------------|
| *endTime*         | *float*           | *final simulation time*                      |

<br />

# <img src="Python.svg" width="60"/> PFEM3D File

<br />

The input file for the fluid solver is the standard Lua for [PFEM3D](https://github.CW/ImperatorS79/PFEM3D). Because the time step and total simulation time are controlled by FSPC, the related variables in `Problem.Solver` are not used. It is also recommended setting the parameter `adaptDT` to `true` and disabling the automatic remeshing because FSPC is already performing a remeshing at the end of each coupling time step.

<br />

```lua
Problem.autoRemeshing = false       -- Disable the automatic remeshing
Problem.Solver.adaptDT = true       -- Enable adaptive time step
```

<br />

In order to enable the FSI coupling, it is mandatory to give the name `FSInterface` to the physical group representing your fluid-structure interface in Gmsh, and activate the external boundary conditions on this interface. This allows FSPC to dynamically enforce a Dirichlet condition on the nodes of this physical group.

<br />

```lua
Problem.Mesh.mshFile = 'geometry.msh'                   -- Load the fluid mesh
Problem.Solver.HeatEq.BC['FSInterfaceTExt'] = true      -- Enable thermal coupling
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true   -- Enable mechanical coupling
```

<br />

# <img src="Python.svg" width="60"/> Metafor File

<br />

The input file for the solid solver is the standard Python for [Metafor](http://metafor.ltas.ulg.ac.be/dokuwiki/). Because FSPC manages the time step and simulation time, the functions `tsm.setInitialTime` and `tsm.setNextTime` must be discarded from your Metafor input file, but all other functions can be used safely. Moreover, FSPC has only been tested with Gmsh import.

<br />

```python
import toolbox.gmsh as gmsh                             # Import the Gmsh toolbox
importer = gmsh.GmshImport('geometry.msh',domain)       # Load the mesh file
importer.execute()                                      # Translate the mesh into Metafor
```

<br />

The object `domain` refers to the Metafor domain. The name of the physical group related to the fluid-structure interface can be chosen freely, but the corresponding nodes must be stored in the `FSInterface` entry of the parameter dictionary retrieved from `getMetafor(parm)`. An example with the Gmsh importer:

<br />

```python
groups = importer.groups                            # Dict of all physical groups in Gmsh
parm['FSInterface'] = groups['myInterface']         # myInterace is the FSI physical group
```

<br />

The FSI coupling is performed with the help of a nodal interaction allowing to dynamically set a Dirichlet condition on the corresponding nodes. Note that each interaction must be specified independently for each type of element. Moreover, thermal and mechanical interaction classes are stored in different objects. 

<br />

```python
prp = ElementProperties(NodStress2DElement)         # Nodal stress interaction elements
load = NodInteraction(1)                            # Object of mechanical interaction
load.push(groups['FSInterface'])                    # Add the nodes from the interface
load.addProperty(prp)                               # Add the element poroperty
```

```python
prp = ElementProperties(NodHeatFlux2DElement)       # Nodal flux interaction elements
heat = NodInteraction(2)                            # Object of thermal interaction
heat.push(groups['FSInterface'])                    # Add the nodes from the interface
heat.addProperty(prp)                               # Add the element poroperty
```

<br />

The resulting nodal interactions must be provided to FSPC through the parameter dictionary. Note that the type of coupling must be consistent with the one defined in the main Python script, meaning that if `convMech` is defined in FSPC, the algorithm will look for `load` in Metafor and if `convTher` is defined, it will look for the corresponding `heat` interaction.

<br />

```python
parm['interacT'] = heat        # Send the heat interaction to FSPC
parm['interacM'] = load        # Send the mechanical interaction to FSPC
```

<br />

Finally, the user may define an exporter class that will be called by FSPC to write the current state of the solution on the disk. This class must contain an `execute` function that should be callable during the simulation. Metafor already contains a built-in class with such method, allowing to export the current solution in a Gmsh file.

<br />

```python
parm['exporter'] = gmsh.GmshExport('output.msh',metafor)       # Create the Gmsh exporter class
parm['exporter'].addInternalField([IF_EVMS,IF_P])              # Add the stress and pressure fields
parm['exporter'].addDataBaseField([TO])                        # Add the temperature field
```