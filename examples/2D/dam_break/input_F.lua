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
Problem.Mesh.localHcharGroups = {'FSInterface', 'Reservoir', 'FreeSurface'}
Problem.Mesh.deleteBoundElements = {'FSInterface'}
Problem.Mesh.boundingBox = {0, 0, 0.584, 0.584}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.7
Problem.Mesh.gamma = 0.5
Problem.Mesh.hchar = 0.005
Problem.Mesh.gammaFS = 0.5
Problem.Mesh.minHeightFactor = 1e-3

Problem.Mesh.addOnFS = false
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteFlyingNodes = false

-- Extractor Parameters

Problem.Extractors = {}
Problem.Extractors[0] = {}
Problem.Extractors[0].kind = 'GMSH'
Problem.Extractors[0].writeAs = 'NodesElements'
Problem.Extractors[0].outputFile = 'pfem/output.msh'
Problem.Extractors[0].whatToWrite = {'p', 'velocity'}
Problem.Extractors[0].timeBetweenWriting = math.huge

Problem.Extractors[1] = {}
Problem.Extractors[1].kind = 'Global'
Problem.Extractors[1].whatToWrite = 'mass'
Problem.Extractors[1].outputFile = 'mass.txt'
Problem.Extractors[1].timeBetweenWriting = math.huge

-- Material Parameters

Problem.Material = {}
Problem.Material.mu = 1e-3
Problem.Material.gamma = 7e-2
Problem.Material.rho = 1000

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
Problem.Solver.MomContEq.nlAlgo = 'NR'
Problem.Solver.MomContEq.residual = 'Ax_f'
Problem.Solver.MomContEq.sparseSolverLib = 'MKL'

Problem.Solver.MomContEq.pExt = 0
Problem.Solver.MomContEq.maxIter = 25
Problem.Solver.MomContEq.minRes = 1e-8
Problem.Solver.MomContEq.bodyForce = {0, -9.81}

-- Fluid Structure Interface

Problem.IC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true

-- Boundary Condition Functions

function Problem.IC.initStates(x, y, z)
	return {0, 0, 0}
end

function Problem.Solver.MomContEq.BC.ReservoirV(x, y, z, t)
	return 0, 0
end

function Problem.Mesh.computeHcharFromDistance(x, y, z, t, dist)
	return Problem.Mesh.hchar+dist*0.1
end
