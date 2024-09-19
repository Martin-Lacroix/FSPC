-- Problem Parameters

Problem = {}
Problem.id = 'ThermoMechanicalBoussinesq'

Problem.verboseOutput = true
Problem.autoRemeshing = false
Problem.simulationTime = math.huge

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
Problem.Extractors[1] = {}
Problem.Extractors[1].kind = 'GMSH'
Problem.Extractors[1].writeAs = 'NodesElements'
Problem.Extractors[1].outputFile = 'pfem/output.msh'
Problem.Extractors[1].whatToWrite = {'T', 'velocity'}
Problem.Extractors[1].timeBetweenWriting = math.huge

Problem.Extractors[2] = {}
Problem.Extractors[2].kind = 'Global'
Problem.Extractors[2].whatToWrite = 'mass'
Problem.Extractors[2].outputFile = 'mass.txt'
Problem.Extractors[2].timeBetweenWriting = math.huge

-- Material Parameters

Problem.Material = {}
Problem.Material[1] = {}

Problem.Material[1].StateEquation = {}
Problem.Material[1].StateEquation.type = 'Incompressible'
Problem.Material[1].StateEquation.rho = 1000

Problem.Material[1].CaloricStateEq = {}
Problem.Material[1].CaloricStateEq.type = 'LinearHeatCapacity'
Problem.Material[1].CaloricStateEq.cp = 1000
Problem.Material[1].CaloricStateEq.DcpDT = 0
Problem.Material[1].CaloricStateEq.Tr = 340

Problem.Material[1].HeatFlux = {}
Problem.Material[1].HeatFlux.type = 'LinearFourierFlux'
Problem.Material[1].HeatFlux.k = 50
Problem.Material[1].HeatFlux.DkDT = 0
Problem.Material[1].HeatFlux.Tr = 340

Problem.Material[1].CoolingLaw = {}
Problem.Material[1].CoolingLaw.type = 'LinearCoolingLaw'
Problem.Material[1].CoolingLaw.h = 0.0
Problem.Material[1].CoolingLaw.Tinf = 340

Problem.Material[1].OpticalProperties = {}
Problem.Material[1].OpticalProperties.type = 'ConstantOpticalProperties'
Problem.Material[1].OpticalProperties.emissivity = 0
Problem.Material[1].OpticalProperties.sigmaSB = 0
Problem.Material[1].OpticalProperties.absorptivity = 0
Problem.Material[1].OpticalProperties.Tinf = 340

Problem.Material[1].Stress = {}
Problem.Material[1].Stress.type = 'NewtonianFluid'
Problem.Material[1].Stress.mu = 1e-2

Problem.Material[1].SurfaceStress = {}
Problem.Material[1].SurfaceStress.type = 'SurfaceTension'
Problem.Material[1].SurfaceStress.gamma = 0

-- Solver Parameters

Problem.Solver = {}
Problem.Solver.IC = {}
Problem.Solver.type = 'Implicit'

Problem.Solver.adaptDT = true
Problem.Solver.maxDT = math.huge
Problem.Solver.initialDT = math.huge
Problem.Solver.solveHeatFirst = false

Problem.Solver.coeffDTDecrease = 2
Problem.Solver.coeffDTincrease = 1

-- Momentum Continuity Equation

Problem.Solver.MomContEq = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true

Problem.Solver.MomContEq.nlAlgo = 'Picard'
Problem.Solver.MomContEq.residual = 'U_P'
Problem.Solver.MomContEq.stabilization = 'FracStep'
Problem.Solver.MomContEq.timeIntegration = 'BackwardEuler'

Problem.Solver.MomContEq.pExt = 0
Problem.Solver.MomContEq.maxIter = 25
Problem.Solver.MomContEq.gammaFS = 0.5
Problem.Solver.MomContEq.minRes = 1e-6
Problem.Solver.MomContEq.tolerance = 1e-16
Problem.Solver.MomContEq.bodyForce = {0, 0, -9.81}

-- Heat Equation

Problem.Solver.HeatEq = {}
Problem.Solver.HeatEq.BC = {}
Problem.Solver.HeatEq.BC['FSInterfaceTExt'] = true

Problem.Solver.HeatEq.nlAlgo = 'Picard'
Problem.Solver.HeatEq.residual = 'Ax_f'
Problem.Solver.HeatEq.timeIntegration = 'BackwardEuler'

Problem.Solver.HeatEq.maxIter = 25
Problem.Solver.HeatEq.minRes = 1e-6
Problem.Solver.HeatEq.tolerance = 1e-16

-- Fluid Structure Interface

Problem.Solver.IC = {}
Problem.Solver.HeatEq.BC = {}
Problem.Solver.MomContEq.BC = {}
Problem.Solver.HeatEq.BC['FSInterfaceTExt'] = true
Problem.Solver.MomContEq.BC['FSInterfaceVExt'] = true

-- Initial Conditions

function Problem.Solver.IC.initStates(x, y, z)
	return {0, 0, 0, 0, 340}
end

-- Momentum Continuity Equation BC

function Problem.Solver.MomContEq.BC.ContainerV(x, y, z, t)
	return 0, 0, 0
end

-- Heat Equation BC

function Problem.Solver.HeatEq.BC.ContainerQ(x, y, z, t)
    return 0, 0, 0
end

function Problem.Solver.HeatEq.BC.FreeSurfaceQ(x, y, z, t)
    return 0, 0, 0
end

-- Characteristic Size

function Problem.Mesh.computeHcharFromDistance(x, y, z, t, dist)
    return Problem.Mesh.hchar+dist*0.05
end