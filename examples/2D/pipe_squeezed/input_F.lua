-- Problem Parameters

Problem = {}
Problem.id = 'Mechanical'

Problem.verboseOutput = false
Problem.autoRemeshing = false
Problem.simulationTime = math.huge

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'CGAL_Edge'
Problem.Mesh.mshFile = 'geometry_F.msh'
Problem.Mesh.deleteBoundElements = {'FSInterface'}
Problem.Mesh.boundingBox = {-1, -2.625, 1, 2.375}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.5
Problem.Mesh.gamma = 0.3
Problem.Mesh.hchar = 0.04
Problem.Mesh.gammaFS = 0.2
Problem.Mesh.gammaBound = 0.2
Problem.Mesh.minHeightFactor = 1e-3

Problem.Mesh.addOnFS = true
Problem.Mesh.keepFluidElements = false
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
Problem.Material[1].Stress.mu = 1e-3

Problem.Material[1].StateEquation = {}
Problem.Material[1].StateEquation.type = 'TaitMurnaghan'
Problem.Material[1].StateEquation.K0 = 100
Problem.Material[1].StateEquation.K0p = 1
Problem.Material[1].StateEquation.rho0 = 1e-6
Problem.Material[1].StateEquation.p0 = 0

Problem.Material[1].SurfaceStress = {}
Problem.Material[1].SurfaceStress.type = 'SurfaceTension'
Problem.Material[1].SurfaceStress.gamma = 0

-- Solver Parameters

Problem.Solver = {}
Problem.Solver.IC = {}
Problem.Solver.type = 'Explicit'
Problem.Solver.timeIntegration = 'CDS'
Problem.Solver.securityCoeff = 0.2

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.maxRemeshDT = math.huge

-- Momentum Equation

Problem.Solver.MomEq = {}
Problem.Solver.MomEq.BC = {}
Problem.Solver.MomEq.pExt = 0
Problem.Solver.MomEq.bodyForce = {0, 0}
Problem.Solver.MomEq.BC['FSInterfaceVExt'] = true

-- Continuity Equation

Problem.Solver.ContEq = {}
Problem.Solver.ContEq.BC = {}
Problem.Solver.ContEq.version = 'DpDt'
Problem.Solver.ContEq.stabilization = 'CLS'

-- Initial Conditions

function Problem.Solver.IC.initStates(x, y, z)
	return {0, 0, 0, Problem.Material[1].StateEquation.rho0, 0, 0}
end

-- Momentum Equation BC

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