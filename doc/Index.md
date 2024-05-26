# <img src="Python.svg" width="60"/> Main Script

<br />

FSPC provides some classes able to perform FSI simulation by partitioned coupling of a fluid and a structural solver. This package uses MPI for the communication between them, and assumes that the solvers are available in your path. An example of how to run your Python script with FSPC is provided bellow.

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

The first step is to import the package with `import FSPC`. The latter initializes MPI and provides a method to initialize the external solver wrappers with their respective input files. At that point, the script is run on two MPI processes. You may call `FSPC.general.is_fluid` or `FSPC.general.is_solid` to check if the current MPI process is related to the fluid of the solid solver.

<br />

```python
solver = FSPC.init_solver(path_F, path_S)
```

| Input             | Type              | Description                                    |
|-------------------|-------------------|------------------------------------------------|
| *path_F*          | *string*          | *path to the input file of the fluid solver*   |
| *path_S*          | *string*          | *path to the input file of the solid solver*   |

<br />

The algorithm is set as follows. The class `BGS` holds for block-Gauss Seidel with Aitken relaxation and possesses and internal parameter `algorithm.omega` for the initial value of the relaxation, which is `0.5` by default. The class `ILS` holds for interface quasi-Newton with inverse least squares and will perform a `BGS` iteration when no previous residual vector is available. The class `MVJ` holds for interface quasi-Newton with multi-vector Jacobian and is an improved version of the `ILS` that reuses the Jacobian from the previous time step when computing the current one.

<br />

```python
algorithm = FSPC.algorithm.BGS(max_iter)
algorithm = FSPC.algorithm.ILS(max_iter)
algorithm = FSPC.algorithm.MVJ(max_iter)

FSPC.set_algorithm(algorithm)
```

| Input             | Type                | Description                      |
|-------------------|---------------------|----------------------------------|
| *max_iter*        | *int*               | *maximum number of iterations*   |

<br />

The interpolator is used to transfer nodal data from one solver to another. The class `NNS` holds for nearest neighbour search and is valid for matching meshes. The class `LEP` holds for linear element projection and is an extension of the `NNS` for non-matching meshes that uses projections into virtual 2-node segments or 3-node triangle elements to interpolate the data with the shape functions. The `TPS` is a radial-basis function interpolation with thin plate spline. The latter is more robust but involves more computations.

<br />

```python
interpolator = FSPC.interpolator.NNS()
interpolator = FSPC.interpolator.LEP(elem_type)
interpolator = FSPC.interpolator.TPS(radius)

FSPC.set_interpolator(interpolator)
```

| Input             | Type                | Description                                     |
|-------------------|---------------------|-------------------------------------------------|
| *elem_type*         | *int*               | *type of element for projection*                  |
| *radius*         | *float*               | *characteristic radius of the RBF*                  |

<br />

The time step manager is responsible for adapting the time step during the simulation as well as exporting the current solution when asked by the user. The `TimeStep` class may also prematurely end the simulation if the time step reaches a critically small value.

<br />

```python
step = FSPC.general.TimeStep(dt, dt_save)
FSPC.set_time_step(step)
```

| Input             | Type                | Description                                     |
|-------------------|---------------------|-------------------------------------------------|
| *dt*         | *float*               | *initial coupling time step*                  |
| *st_save*         | *float*               | *time step for saving on the disk*                  |

<br />

The residual manager is responsible for checking the convergence of the fluid-structure coupling algorithm. The `Residual` class must be defined for enabling the corresponding coupling type. For instance, calling `FSPC.set_mechanical_res` with a valid input will enable the mechanical coupling. In the same way, calling `FSPC.set_thermal_res` will enable the thermal coupling. Both couplings may also be enabled together for a thermo-mechanical fluid-structure simulation.

<br />

```python
residual = FSPC.general.Residual(tol_disp)
FSPC.set_mechanical_res(residual)

residual = FSPC.general.Residual(tol_temp)
FSPC.set_thermal_res(residual)
```

| Input             | Type                | Description                                     |
|-------------------|---------------------|-------------------------------------------------|
| *tol_disp*         | *float*               | *tolerance for the displacement*                  |
| *tol_temp*         | *float*               | *tolerance for the temperature*                  |

<br />

Once all the other classes have been set in FSPC, you may call `algorithm.simulate` to start the simulation for the desired duration. The computation time of different functions are computed during the simulation and can be displayed in the terminal at the end.

<br />

```python
algorithm.simulate(end_time)
FSPC.general.print_clock()
```

| Input             | Type                | Description                                     |
|-------------------|---------------------|-------------------------------------------------|
| *end_time*         | *float*               | *final simulation time*                  |

<br />

# <img src="Python.svg" width="60"/> PFEM3D File

<br />

The input file for the fluid solver is the standard Lua for [PFEM3D](https://github.com/ImperatorS79/PFEM3D). First, it is mandatory to disable the automatic remeshing in PFEM3D because FSPC will automatically call the remeshing function at the end of each coupling time step and update its internal variables accordingly. Thereby, letting the following variable to `true` may lead to incorrect results.

<br />

```lua
Problem.autoRemeshing = false
```

<br />

In order to enable the FSI coupling, it is mandatory to give the name `FSInterface` to the physical group representing your fluid-structure interface, and activate the external boundary conditions on this interface. This allows FSPC to dynamically enforce a Dirichlet condition on the nodes. For instance, the external temperature and velocity conditions are enabled for an incompressible fluid as follows.

<br />

```lua
Problem.Solver.HeatEq.BC['FSInterfaceTExt'] = true
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true
```

<br />

Because the progress of the fluid-structure simulation is managed by FSPC, some parameters in PFEM3D are not used. However, the fluid solver may still require them to be initialized in the Lua file. It is recommended to give them a high value to ensure that nothing disrupts the coupling. The list of unused parameters is given below.

<br />

```lua
Problem.simulationTime = math.huge
Problem.Extractors.timeBetweenWriting = math.huge

Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
```

<br />

# <img src="Python.svg" width="60"/> Metafor File

<br />

The input file for the solid solver is the standard Python for [Metafor](http://metafor.ltas.ulg.ac.be/dokuwiki/). The Metafor wrapper is imported with `import wrap as w`. The following example shows how to load a Gmsh file in Metafor and set the mandatory parameters for FSPC.

<br />

```python
import toolbox.gmsh as gmsh

metafor = w.Metafor()
importer = w.GmshImport('geometry.msh', metafor.getDomain())
importer.execute()
```

<br />

The name of the physical group related to the fluid-structure interface can be chosen freely, but the corresponding nodes must be stored in the `FSInterface` entry of the parameter dictionary retrieved from `getMetafor(parm)`.

<br />

```python
groups = importer.groups
parm['FSInterface'] = groups['myInterface']
```

<br />

The coupling is performed with the help of a nodal interaction allowing to dynamically set a Neumann condition on the corresponding nodes. Note that each interaction must be specified independently for each type of element. The following example shows how to define a mechanical interaction compatible with FSPC.

<br />

```python
prp = ElementProperties(NodStress2DElement)

interaction_M = NodInteraction(1)
interaction_M.push(groups['FSInterface'])
interaction_M.addProperty(prp)
```

<br />

The resulting nodal interactions must be provided to FSPC through the parameter dictionary. Note that the type of coupling must be consistent with the one defined in the main Python script, meaning that if `FSPC.set_mechanical_res` has been called in the main script, FSPC will look for `interaction_M` within Metafor. Equivalently, if `FSPC.set_thermal_res` has been called, it will look for the corresponding `interaction_T` interaction.

<br />

```python
parm['interaction_M'] = interaction_M
parm['interaction_T'] = interaction_T
```

<br />

Finally, the user may define an exporter class that will be called by FSPC to write the current state of the solution on the disk. This class must contain the `write` function that should be callable during the simulation. Metafor already contains a built-in class with such method, allowing to export the current solution in a Gmsh file.

<br />

```python
ext = w.GmshExporter(metafor, 'output')
ext.add(w.IFNodalValueExtractor(groups['Solid'], w.IF_EVMS))
parm['exporter'] = ext
```

<br />

It is important to note that because FSPC manages the progress of the fluid-structure simulation, you should not initialize or call `setInitialTime` and `setNextTime` from `metafor.getTimeStepManager` in the input file.