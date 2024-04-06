-- Problem Parameters

Problem = {}
Problem.verboseOutput = false
Problem.autoRemeshing = false
Problem.simulationTime = math.huge
Problem.id = 'WCompNewtonNoT'

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'GMSH'
Problem.Mesh.mshFile = 'geometry_F.msh'
Problem.Mesh.boundingBox = {-1, -2.625, 1, 2.375}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.5
Problem.Mesh.gamma = 0.3
Problem.Mesh.hchar = 0.04
Problem.Mesh.gammaFS = 0.2
Problem.Mesh.minHeightFactor = 1e-3

Problem.Mesh.addOnFS = true
Problem.Mesh.keepFluidElements = false
Problem.Mesh.deleteFlyingNodes = false
Problem.Mesh.deleteBoundElements = true

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
Problem.Material.p0 = 0
Problem.Material.mu = 1e-5
Problem.Material.K0p = 1
Problem.Material.gamma = 0
Problem.Material.K0 = 100
Problem.Material.rhoStar = 1e-6

-- Solver Parameters

Problem.Solver = {}
Problem.Solver.id = 'CDS_dpdt'
Problem.Solver.securityCoeff = 0.2

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.maxRemeshDT = math.huge

-- Momentum Continuity Equation

Problem.Solver.MomEq = {}
Problem.Solver.ContEq = {}
Problem.Solver.MomEq.pExt = 0
Problem.Solver.MomEq.bodyForce = {0, 0}
Problem.Solver.ContEq.stabilization = 'CLS'

-- Momentum Continuity BC

Problem.IC = {}
Problem.Solver.MomEq.BC = {}
Problem.Solver.ContEq.BC = {}
Problem.Solver.MomEq.BC['FSInterfaceVExt'] = true

function Problem.IC.initStates(x, y, z)
	return {0, 0, 0, Problem.Material.rhoStar, 0, 0}
end

function Problem.Solver.MomEq.BC.WallV(x, y, z, t)
	return 0, 0
end

function Problem.Solver.MomEq.BC.InletVEuler(x, y, z, t)

	local amax = -4e5
	local tmax = 2.5e-4
	local r = math.abs(x)
	local R = 1

	if (t < tmax) then
		local a = amax*(1-(r*r)/(R*R))
		return 0, a

	else
		return 0, 0
	end
end