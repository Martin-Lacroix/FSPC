-- Problem Parameters

Problem = {}
Problem.verboseOutput = true
Problem.autoRemeshing = false
Problem.simulationTime = math.huge
Problem.id = 'Boussinesq'

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.5
Problem.Mesh.gamma = 0.6
Problem.Mesh.hchar = 3.7e-3
Problem.Mesh.gammaFS = 0.2
Problem.Mesh.addOnFS = false
Problem.Mesh.minAspectRatio = 1e-3
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteFlyingNodes = true
Problem.Mesh.deleteBoundElements = false
Problem.Mesh.boundingBox = {-0.1,-0.1,0,0.1,0.1,1}
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
Problem.Material.mu = 1e-2
Problem.Material.gamma = 0
Problem.Material.rho = 1000
Problem.Material.epsRad = 0
Problem.Material.sigmaRad = 0
Problem.Material.R = 8.31446261815324
Problem.Material.alphaLin = 0
Problem.Material.DgammaDT = 0
Problem.Material.Tinf = 340
Problem.Material.cp = 1000
Problem.Material.DmuDT = 0
Problem.Material.DcpDT = 0
Problem.Material.DkDT = 0
Problem.Material.Tr = 340
Problem.Material.k = 50
Problem.Material.h = 1

-- Solver Parameters

Problem.Solver = {}
Problem.Solver.id = 'FracStep'

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.coeffDTDecrease = math.huge
Problem.Solver.coeffDTincrease = math.huge
Problem.Solver.solveHeatFirst = true

-- Momentum Continuity Equation

Problem.Solver.MomContEq = {}
Problem.Solver.MomContEq.residual = 'U_P'
Problem.Solver.MomContEq.nlAlgo = 'Picard'

Problem.Solver.MomContEq.pExt = 0
Problem.Solver.MomContEq.maxIter = 25
Problem.Solver.MomContEq.gammaFS = 0.5
Problem.Solver.MomContEq.minRes = 1e-8
Problem.Solver.MomContEq.cgTolerance = 1e-16
Problem.Solver.MomContEq.bodyForce = {0,0,-9.81}

-- Heat Equation

Problem.Solver.HeatEq = {}
Problem.Solver.HeatEq.residual = 'Ax_f'
Problem.Solver.HeatEq.nlAlgo = 'Picard'
Problem.Solver.HeatEq.sparseSolver = 'CG'

Problem.Solver.HeatEq.maxIter = 25
Problem.Solver.HeatEq.minRes = 1e-6
Problem.Solver.HeatEq.cgTolerance = 1e-16

-- Heat Momentum Continuity BC

Problem.IC = {}
Problem.Solver.HeatEq.BC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.HeatEq.BC['FSInterfaceTExt'] = true
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true

function Problem.IC.initStates(x,y,z)
	return {0,0,0,0,340}
end

function Problem.Solver.MomContEq.BC.WallV(x,y,z,t)
	return 0,0,0
end

function Problem.Solver.HeatEq.BC.WallQ(x,y,z,t)
    return 0,0,0
end

function Problem.Solver.HeatEq.BC.FreeSurfaceQ(x,y,z,t)
    return 0,0,0
end