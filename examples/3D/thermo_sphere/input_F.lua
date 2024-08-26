-- Problem Parameters

Problem = {}
Problem.verboseOutput = true
Problem.autoRemeshing = false
Problem.simulationTime = math.huge
Problem.id = 'Boussinesq'

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'Tetgen_Edge'
Problem.Mesh.mshFile = 'geometry_F.msh'
Problem.Mesh.localHcharGroups = {'FSInterface'}
Problem.Mesh.deleteBoundElements = {'FSInterface'}
Problem.Mesh.boundingBox = {-0.1, -0.1, 0, 0.1, 0.1, 1}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.7
Problem.Mesh.gamma = 0.3
Problem.Mesh.hchar = 3e-3
Problem.Mesh.gammaFS = 0.2
Problem.Mesh.gammaBound = 0.2
Problem.Mesh.minHeightFactor = 1e-2

Problem.Mesh.addOnFS = false
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteFlyingNodes = true

-- Extractor Parameters

Problem.Extractors = {}
Problem.Extractors[0] = {}
Problem.Extractors[0].kind = 'GMSH'
Problem.Extractors[0].writeAs = 'NodesElements'
Problem.Extractors[0].outputFile = 'pfem/output.msh'
Problem.Extractors[0].whatToWrite = {'T', 'velocity'}
Problem.Extractors[0].timeBetweenWriting = math.huge

Problem.Extractors[1] = {}
Problem.Extractors[1].kind = 'Global'
Problem.Extractors[1].whatToWrite = 'mass'
Problem.Extractors[1].outputFile = 'mass.txt'
Problem.Extractors[1].timeBetweenWriting = math.huge

-- Material Parameters

Problem.Material = {}
Problem.Material.mu = 1e-2
Problem.Material.rho = 1000
Problem.Material.R = 8.31446261815324
Problem.Material.cp = 1000
Problem.Material.k = 50

Problem.Material.gamma = 0
Problem.Material.epsRad = 0
Problem.Material.sigmaRad = 0
Problem.Material.alphaLin = 0
Problem.Material.DgammaDT = 0
Problem.Material.DmuDT = 0
Problem.Material.DcpDT = 0
Problem.Material.DkDT = 0
Problem.Material.Tinf = 0
Problem.Material.Tr = 0
Problem.Material.h = 0

-- Solver Parameters

Problem.Solver = {}
Problem.Solver.id = 'FracStep'

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.solveHeatFirst = false

Problem.Solver.coeffDTDecrease = 2
Problem.Solver.coeffDTincrease = 1

-- Momentum Continuity Equation

Problem.Solver.MomContEq = {}
Problem.Solver.MomContEq.residual = 'U_P'
Problem.Solver.MomContEq.nlAlgo = 'Picard'

Problem.Solver.MomContEq.pExt = 0
Problem.Solver.MomContEq.maxIter = 25
Problem.Solver.MomContEq.gammaFS = 0.5
Problem.Solver.MomContEq.minRes = 1e-6
Problem.Solver.MomContEq.tolerance = 1e-16
Problem.Solver.MomContEq.bodyForce = {0, 0, -9.81}

-- Heat Equation

Problem.Solver.HeatEq = {}
Problem.Solver.HeatEq.residual = 'Ax_f'
Problem.Solver.HeatEq.nlAlgo = 'Picard'

Problem.Solver.HeatEq.maxIter = 25
Problem.Solver.HeatEq.minRes = 1e-6
Problem.Solver.HeatEq.tolerance = 1e-16

-- Fluid Structure Interface

Problem.Solver.IC = {}
Problem.Solver.HeatEq.BC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.HeatEq.BC['FSInterfaceTExt'] = true
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true

-- Boundary Condition Functions

function Problem.Solver.IC.initStates(x, y, z)
	return {0, 0, 0, 0, 340}
end

function Problem.Solver.MomContEq.BC.ContainerV(x, y, z, t)
	return 0, 0, 0
end

function Problem.Solver.HeatEq.BC.ContainerQ(x, y, z, t)
    return 0, 0, 0
end

function Problem.Solver.HeatEq.BC.FreeSurfaceQ(x, y, z, t)
    return 0, 0, 0
end

function Problem.Mesh.computeHcharFromDistance(x, y, z, t, dist)
    return Problem.Mesh.hchar+dist*0.05
end