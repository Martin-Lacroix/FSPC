Problem = {

    -- Main simulation parameters

    mechanical = true,
    verboseOutput = true,
    autoRemeshing = false,
    simulationTime = math.huge
}

Problem.Mesh = {

    -- Input mesh and bounding box

    remeshAlgo = 'Tetgen_Edge',
    mshFile = 'geometry_F.msh',
    deleteBoundElements = {'FSI'},
    boundingBox = {-1, -0.028, -1, 1, 0.028, 1},
    exclusionZones = {},

    -- Remeshing internal parameters

    alpha = 1.2,
    omega = 0.7,
    gamma = 0.3,
    hchar = 5e-3,
    gammaFS = 0.2,
    epsilonLS = 0.2,
    gammaEdge = 0.2,
    minHeightFactor = 1e-3,

    -- Enable or disable algorithms

    addOnFS = true,
    useLevelSet = true,
    keepFluidElements = true,
    deleteFlyingNodes = true
}

Problem.Extractors = {}

-- Add an extractor for each output kind

Problem.Extractors[1] = {

    -- Export the mesh in a GMSH file

    kind = 'GMSH',
    writeAs = 'NodesElements',
    outputFile = 'pfem/output.msh',
    whatToWrite = {'p', 'velocity'},
    timeBetweenWriting = math.huge
}

Problem.Extractors[2] = {

    -- Export the total fluid mass

    kind = 'Global',
    whatToWrite = 'mass',
    outputFile = 'mass.txt',
    timeBetweenWriting = math.huge
}

Problem.Material = {}

-- First material is the fluid

Problem.Material[1] = {

    -- Parameters for the viscosity

    Stress = {
        type = 'NewtonianFluid',
        mu = 5e-2
    },
    
    -- Parameters for the fluid bulk

    StateEquation = {
        type = 'Incompressible',
        rho = 917
    },

    -- Parameters for surface tension

    SurfaceStress = {
        type = 'SurfaceTension',
        gamma = 0
    }
}

Problem.Solver = {

    -- Initial conditions and type

    IC = {},
    type = 'Implicit',

    -- Factors of time step changes

    coeffDTDecrease = 2,
    coeffDTincrease = 1,

    -- Enable or disable algorithms

    adaptDT = true,
    maxDT = math.huge,
    initialDT = math.huge
}

Problem.Solver.MomContEq = {

    -- Enable the fluid-structure interface

    BC = {FSIVExt = true},

    -- Define the solver algorithms

    nlAlgo = 'Picard',
    systemForm = 'FracStep',
    timeIntegration = 'BackwardEuler',
    residual = 'U_P',

    -- Other simulation parameters

    pExt = 0,
    maxIter = 25,
    gammaFS = 0.5,
    minRes = 1e-6,
    tolerance = 1e-12,
    bodyForce = {0, 0, -9.81},
}

-- Initial Conditions

function Problem.Solver.IC.initStates(x, y, z)
    return {0, 0, 0, 0}
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

    local r = math.sqrt(x^2+z^2)
    local theta = math.atan(z, x)

    local x_dt = -r*math.sin(theta)*theta_dt
    local z_dt = r*math.cos(theta)*theta_dt

    return x_dt, 0, z_dt
end
