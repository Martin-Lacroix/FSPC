-- Problem Parameters

Problem = {}
Problem.id = 'Mechanical'

Problem.verboseOutput = true
Problem.autoRemeshing = false
Problem.simulationTime = math.huge

-- Mesh Parameters

Problem.Mesh = {}
Problem.Mesh.remeshAlgo = 'CGAL_Edge'
Problem.Mesh.mshFile = 'geometry_F.msh'
Problem.Mesh.deleteBoundElements = {'FSInterface'}
Problem.Mesh.localHcharGroups = {'FSInterface', 'Container', 'FreeSurface'}
Problem.Mesh.boundingBox = {-1, -1, 1, 1}
Problem.Mesh.exclusionZones = {}

Problem.Mesh.alpha = 1.2
Problem.Mesh.omega = 0.7
Problem.Mesh.gamma = 0.3
Problem.Mesh.hchar = 5e-3
Problem.Mesh.gammaFS = 0.2
Problem.Mesh.alphaOut = 0.6
Problem.Mesh.gammaEdge = 0.2
Problem.Mesh.minHeightFactor = 1e-3

Problem.Mesh.addOnFS = true
Problem.Mesh.keepFluidElements = true
Problem.Mesh.deleteFlyingNodes = true

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
Problem.Material[1].Stress.mu = 5e-2

Problem.Material[1].StateEquation = {}
Problem.Material[1].StateEquation.type = 'Incompressible'
Problem.Material[1].StateEquation.rho = 917

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
Problem.Solver.MomContEq.bodyForce = {0, -9.81}

-- Initial Conditions

function Problem.Solver.IC.initStates(x, y, z)
    return {0, 0, 0}
end

-- Momentum Continuity Equation BC

function Problem.Solver.MomContEq.BC.ContainerV(x, y, z, t)

    local S = 2.144
    local K = 4.9
    local R = 2.278
    local Q = 1.278

    -- Denominator inside the sine for theta

    local den = Q*(1+math.exp(S-K*t))
        + (R-Q)*math.exp(S-K*t)/(1+math.exp(t))
        + (R-Q)/(1+math.exp(t))

    local den_dt = -K*Q*math.exp(S-K*t)
        - (R-Q)*math.exp(t)/(math.exp(t)+1)^2
        + (Q-R)*(K*math.exp(-t)+1+K)*math.exp(-t-K*t+S)/(math.exp(-t)+1)^2

    -- Numerator insine the sine for theta

    local num = 2*math.pi*t
    local num_dt = 2*math.pi

    -- Compute the angular velocity in radian

    local fun_dt = (num_dt*den-num*den_dt)/den^2
    local theta_dt = 4*math.cos(num/den)*fun_dt*(math.pi/180)

    -- Convert polar to cartesian velocity

    local r = math.sqrt(x^2+y^2)
    local theta = math.atan(y, x)

    local x_dt = -r*math.sin(theta)*theta_dt
    local y_dt = r*math.cos(theta)*theta_dt

    return x_dt, y_dt
end

-- Characteristic Size

function Problem.Mesh.computeHcharFromDistance(x, y, z, t, dist)
	return Problem.Mesh.hchar+dist*0.1
end
