-- Problem Parameters

Problem = {}
Problem.verboseOutput = true
Problem.autoRemeshing = false
Problem.simulationTime = math.huge
Problem.id = 'IncompNewtonNoT'

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'Tetgen_Edge'
Problem.Mesh.mshFile = 'geometry_F.msh'
Problem.Mesh.localHcharGroups = {'FSInterface'}
Problem.Mesh.deleteBoundElements = {'FSInterface'}
Problem.Mesh.boundingBox = {0, 0, 0, 0.35, 0.25, 0.4}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.7
Problem.Mesh.gamma = 0.3
Problem.Mesh.hchar = 2e-3
Problem.Mesh.gammaFS = 0.2
Problem.Mesh.gammaBound = 0.2
Problem.Mesh.minHeightFactor = 1e-3

Problem.Mesh.addOnFS = true
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
Problem.Material[1].Stress.mu = 1

Problem.Material[1].StateEquation = {}
Problem.Material[1].StateEquation.type = 'Incompressible'
Problem.Material[1].StateEquation.rho = 1220

Problem.Material[1].SurfaceStress = {}
Problem.Material[1].SurfaceStress.type = 'SurfaceTension'
Problem.Material[1].SurfaceStress.gamma = 0

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
Problem.Solver.MomContEq.bodyForce = {0, 0, 0}

-- Fluid Structure Interface

Problem.Solver.IC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true

-- Boundary Condition Functions

function Problem.Solver.IC.initStates(x, y, z)
    return {0, 0, 0, 0}
end

function Problem.Solver.MomContEq.BC.InletVEuler(x, y, z, t)

    local tmax = 0.1
    local vmax = 0.5
    local v = vmax*t/tmax
    
    if (t < tmax) then
	    return v, 0, 0
	else
	    return vmax, 0, 0
    end
end

function Problem.Solver.MomContEq.BC.BottomVEuler(x, y, z, t)
	return 0, 0, 0
end

function Problem.Solver.MomContEq.BC.OutletP(x, y, z, t)
	return 0
end

function Problem.Mesh.computeHcharFromDistance(x, y, z, t, dist)
	return Problem.Mesh.hchar+dist*0.1
end