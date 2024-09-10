-- Problem Parameters

Problem = {}
Problem.verboseOutput = true
Problem.autoRemeshing = false
Problem.simulationTime = math.huge
Problem.id = 'IncompNewtonNoT'

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'CGAL_Edge'
Problem.Mesh.mshFile = 'geometry_F.msh'
Problem.Mesh.boundingBox = {0, -10, 1, 1}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.5
Problem.Mesh.gamma = 0.6
Problem.Mesh.hchar = 0.05
Problem.Mesh.gammaFS = 0.2
Problem.Mesh.gammaBound = 0.2
Problem.Mesh.minHeightFactor = 1e-3

Problem.Mesh.addOnFS = false
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteFlyingNodes = false

-- Extractor Parameters

Problem.Extractors = {}
Problem.Extractors[1] = {}
Problem.Extractors[1].kind = 'GMSH'
Problem.Extractors[1].writeAs = 'NodesElements'
Problem.Extractors[1].outputFile = 'pfem/output.msh'
Problem.Extractors[1].whatToWrite = {'p', 'velocity'}
Problem.Extractors[1].timeBetweenWriting = math.huge

Problem.Extractors[2] = {}
Problem.Extractors[2].kind = 'Global'
Problem.Extractors[2].whatToWrite = 'mass'
Problem.Extractors[2].outputFile = 'mass.txt'
Problem.Extractors[2].timeBetweenWriting = math.huge

-- Material Parameters

Problem.Material = {}
Problem.Material[1] = {}

Problem.Material[1].Stress = {}
Problem.Material[1].Stress.type = 'NewtonianFluid'
Problem.Material[1].Stress.mu = 1e+3

Problem.Material[1].StateEquation = {}
Problem.Material[1].StateEquation.type = 'Incompressible'
Problem.Material[1].StateEquation.rho = 1000

Problem.Material[1].SurfaceStress = {}
Problem.Material[1].SurfaceStress.type = 'SurfaceTension'
Problem.Material[1].SurfaceStress.gamma = 0

-- Solver Parameters

Problem.Solver = {}
Problem.Solver.id = 'PSPG'

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.coeffDTDecrease = 2
Problem.Solver.coeffDTincrease = 1

-- Momentum Continuity Equation

Problem.Solver.MomContEq = {}
Problem.Solver.MomContEq.residual = 'Ax_f'
Problem.Solver.MomContEq.nlAlgo = 'Picard'
Problem.Solver.MomContEq.sparseSolverLib = 'MKL'

Problem.Solver.MomContEq.pExt = 0
Problem.Solver.MomContEq.maxIter = 25
Problem.Solver.MomContEq.minRes = 1e-8
Problem.Solver.MomContEq.bodyForce = {0, -9.81}

-- Fluid Structure Interface

Problem.Solver.IC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true

-- Boundary Condition Functions

function Problem.Solver.IC.initStates(x, y, z)
	return {0, 0, 0}
end

function Problem.Solver.MomContEq.BC.WallV(x, y, z, t)
	return 0, 0
end
