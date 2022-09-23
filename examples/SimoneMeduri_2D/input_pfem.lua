-- Problem Parameters

Problem = {}
Problem.autoRemeshing = false
Problem.verboseOutput = false
Problem.simulationTime = math.huge
Problem.id = 'IncompNewtonNoT'

-- FSPC Parameters

Problem.interface = 'FSInterface'
Problem.maxFactor = 10

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.5
Problem.Mesh.gamma = 0.5
Problem.Mesh.hchar = 0.05
Problem.Mesh.gammaFS = 0.2
Problem.Mesh.addOnFS = false
Problem.Mesh.minAspectRatio = 1e-2
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteFlyingNodes = false
Problem.Mesh.deleteBoundElements = false
Problem.Mesh.laplacianSmoothingBoundaries = false
Problem.Mesh.boundingBox = {-4,-4,4,6.25}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.remeshAlgo = 'GMSH'
Problem.Mesh.mshFile = 'geometry.msh'
Problem.Mesh.exclusionGroups = {'PolyL','PolyR'}
Problem.Mesh.ignoreGroups = {'Solid','SolidExt'}

-- Extractor Parameters

Problem.Extractors = {}

Problem.Extractors[0] = {}
Problem.Extractors[0].kind = 'GMSH'
Problem.Extractors[0].writeAs = 'NodesElements'
Problem.Extractors[0].outputFile = 'pfem/fluid.msh'
Problem.Extractors[0].whatToWrite = {'p','velocity'}
Problem.Extractors[0].timeBetweenWriting = math.huge

Problem.Extractors[1] = {}
Problem.Extractors[1].kind = 'Global'
Problem.Extractors[1].whatToWrite = 'mass'
Problem.Extractors[1].outputFile = 'mass.txt'
Problem.Extractors[1].timeBetweenWriting = math.huge

-- Material Parameters

Problem.Material = {}
Problem.Material.mu = 100
Problem.Material.gamma = 0
Problem.Material.rho = 1000

-- Initial Conditions

Problem.IC = {}
Problem.IC.PolyLFixed = true
Problem.IC.PolyRFixed = true
Problem.IC.ReservoirFixed = true
Problem.IC.FSInterfaceFixed = false

-- Solver Parameters

Problem.Solver = {}
Problem.Solver.id = 'FracStep'

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.coeffDTDecrease = math.huge
Problem.Solver.coeffDTincrease = math.huge

-- Momentum Continuity Equation

Problem.Solver.MomContEq = {}
Problem.Solver.MomContEq.residual = 'U_P'
Problem.Solver.MomContEq.nlAlgo = 'Picard'
Problem.Solver.MomContEq.sparseSolverLib = 'MKL'
Problem.Solver.MomContEq.PStepSparseSolver = 'LLT'

Problem.Solver.MomContEq.pExt = 0
Problem.Solver.MomContEq.maxIter = 25
Problem.Solver.MomContEq.gammaFS = 0.5
Problem.Solver.MomContEq.minRes = 1e-7
Problem.Solver.MomContEq.cgTolerance = 1e-12
Problem.Solver.MomContEq.bodyForce = {0,-9.81}

-- Momentum Continuity BC

Problem.Solver.MomContEq.BC = {}
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true

function Problem.IC:initStates(pos)
	return {0,0,0}
end

function Problem.Solver.MomContEq.BC:ReservoirV(pos,t)
	return {0,0}
end

function Problem.Solver.MomContEq.BC:PolyLV(pos,t)
	return {0,0}
end

function Problem.Solver.MomContEq.BC:PolyRV(pos,t)
	return {0,0}
end

function Problem.Solver.MomContEq.BC:SolidBaseV(pos,t)
	return {0,0}
end
