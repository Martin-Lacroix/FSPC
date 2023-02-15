-- Problem Parameters

Problem = {}
Problem.autoRemeshing = false
Problem.verboseOutput = false
Problem.simulationTime = math.huge
Problem.id = 'IncompNewtonT'

-- FSPC Parameters

Problem.interface = 'FSInterface'
Problem.maxFactor = 10

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.5
Problem.Mesh.gamma = 0.6
Problem.Mesh.hchar = 0.02
Problem.Mesh.gammaFS = 0.2
Problem.Mesh.addOnFS = false
Problem.Mesh.minAspectRatio = 1e-3
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteFlyingNodes = false
Problem.Mesh.deleteBoundElements = false
Problem.Mesh.laplacianSmoothingBoundaries = false
Problem.Mesh.boundingBox = {-0.4,-0.4,0.4,0.4}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.remeshAlgo = 'GMSH'
Problem.Mesh.mshFile = 'geometryF.msh'
Problem.Mesh.exclusionGroups = {'FSInterface'}
Problem.Mesh.ignoreGroups = {}

-- Extractor Parameters

Problem.Extractors = {}

Problem.Extractors[0] = {}
Problem.Extractors[0].kind = 'GMSH'
Problem.Extractors[0].writeAs = 'NodesElements'
Problem.Extractors[0].outputFile = 'pfem/output.msh'
Problem.Extractors[0].whatToWrite = {'T','velocity'}
Problem.Extractors[0].timeBetweenWriting = math.huge

Problem.Extractors[1] = {}
Problem.Extractors[1].kind = 'Global'
Problem.Extractors[1].whatToWrite = 'mass'
Problem.Extractors[1].outputFile = 'mass.txt'
Problem.Extractors[1].timeBetweenWriting = math.huge

-- Material Parameters

Problem.Material = {}
Problem.Material.mu = 5e-3
Problem.Material.gamma = 0
Problem.Material.rho = 1000
Problem.Material.epsRad = 0
Problem.Material.sigmaRad = 0
Problem.Material.R = 8.31446261815324
Problem.Material.alphaLin = 0
Problem.Material.DgammaDT = 0
Problem.Material.Tinf = 340
Problem.Material.cp = 1000
Problem.Material.Tr = 340
Problem.Material.k = 20
Problem.Material.h = 1

-- Solver Parameters

Problem.Solver = {}
Problem.Solver.id = 'PSPG'

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.coeffDTDecrease = math.huge
Problem.Solver.coeffDTincrease = math.huge
Problem.Solver.solveHeatFirst = true

-- Momentum Continuity Equation

Problem.Solver.MomContEq = {}
Problem.Solver.MomContEq.residual = 'Ax_f'
Problem.Solver.MomContEq.nlAlgo = 'Picard'
Problem.Solver.MomContEq.sparseSolverLib = 'MKL'

Problem.Solver.MomContEq.pExt = 0
Problem.Solver.MomContEq.maxIter = 25
Problem.Solver.MomContEq.minRes = 1e-6
Problem.Solver.MomContEq.bodyForce = {0,0}

-- Heat Equation

Problem.Solver.HeatEq = {}
Problem.Solver.HeatEq.residual = 'Ax_f'
Problem.Solver.HeatEq.nlAlgo = 'Picard'
Problem.Solver.HeatEq.sparseSolverLib = 'MKL'

Problem.Solver.HeatEq.maxIter = 25
Problem.Solver.HeatEq.minRes = 1e-6
Problem.Solver.HeatEq.cgTolerance = 1e-9

-- Heat Momentum Continuity BC

Problem.IC = {}
Problem.Solver.HeatEq.BC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.HeatEq.BC['FSInterfaceTExt'] = true

function Problem.IC:initStates(pos)
	return {0,0,0,340}
end

function Problem.Solver.MomContEq.BC:WallV(pos,initPos,state,t)
	return 0,0
end

function Problem.Solver.MomContEq.BC:FSInterfaceV(pos,initPos,state,t)
	return 0,0
end

function Problem.Solver.HeatEq.BC:WallT(pos,initPos,state,t)
    return 340
end