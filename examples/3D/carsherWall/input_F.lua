-- Problem Parameters

Problem = {}
Problem.verboseOutput = true
Problem.autoRemeshing = false
Problem.simulationTime = math.huge
Problem.id = 'IncompNewtonNoT'

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'CGAL'
Problem.Mesh.mshFile = 'geometry_F.msh'
Problem.Mesh.boundingBox = {0, -0.26,-0.26, 1.56, 0.26, 0.26}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.5
Problem.Mesh.gamma = 0.5
Problem.Mesh.hchar = 0.02
Problem.Mesh.gammaFS = 0.5
Problem.Mesh.minHeightFactor = 1e-3

Problem.Mesh.addOnFS = true
Problem.Mesh.keepFluidElements = true
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
Problem.Material.mu = 1e-3
Problem.Material.gamma = 0
Problem.Material.rho = 1000

-- Solver Parameters

Problem.Solver = {}
Problem.Solver.id = 'FracStep'

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
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
Problem.Solver.MomContEq.bodyForce = {0, -9.81, 0}

-- Fluid Structure Interface

Problem.IC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true

-- Boundary Condition Functions

function Problem.IC.initStates(x, y, z)
	return {0, 0, 0, 0}
end

function Problem.Solver.MomContEq.BC.BorderV(x, y, z, t)
	return 0, 0, 0
end

function Problem.Solver.MomContEq.BC.InletVEuler(x, y, z, t)

	local tmax = 1
	local vmax = 10
	local vt = (t/tmax)*vmax
	local r = math.abs(y)
	local R = 0.05

	if (t<tmax) then
		local v = vt*(1-(r*r)/(R*R))
		return v, 0, 0
	else
		
		local v = vmax*(1-(r*r)/(R*R))
		return v, 0, 0
	end
end