Problem = {

    -- Main simulation parameters

    thermal = true,
    mechanical = true,
    boussinesq = true,
    verboseOutput = true,
    autoRemeshing = false,
    simulationTime = math.huge
}

Problem.Mesh = {

    -- Input mesh and bounding box

    remeshAlgo = 'Tetgen_Edge',
    mshFile = 'geometry_F.msh',
    deleteBoundElements = {'FSI'},
    localHcharGroups = {'FSI', 'FreeSurface'},
    boundingBox = {-0.1, -0.1, 0, 0.1, 0.1, 1},
    exclusionZones = {},

    -- Remeshing internal parameters

    alpha = 1.2,
    omega = 0.7,
    gamma = 0.3,
    hchar = 3e-3,
    gammaFS = 0.2,
    gammaEdge = 0.2,
    minHeightFactor = 1e-3,

    -- Enable or disable algorithms

    addOnFS = false,
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
    whatToWrite = {'T', 'velocity'},
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
        mu = 1e-2
    },
    
    -- Parameters for the fluid bulk

    StateEquation = {
        type = 'Incompressible',
        rho = 1000
    },

    -- Parameters for surface tension

    SurfaceStress = {
        type = 'SurfaceTension',
        gamma = 0
    },

    -- Parameters for heat capacity

    CaloricStateEq = {
        type = 'LinearHeatCapacity',
        DcpDT = 0,
        cp = 1000,
        Tr = 340
    },

    -- Parameters for Fourier flux

    HeatFlux = {
        type = 'LinearFourierFlux',
        DkDT = 0,
        Tr = 340,
        k = 50
    },

    -- Parameters for cooling law
    
    CoolingLaw = {
        type = 'LinearCoolingLaw',
        Tinf = 340,
        h = 0
    },

    -- Parameters for optical material
    
    OpticalProperties = {
        type = 'ConstantOpticalProperties',
        absorptivity = 0,
        emissivity = 0,
        sigmaSB = 0,
        Tinf = 340
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
    initialDT = math.huge,
    solveHeatFirst = false
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
    tolerance = 1e-16,
    bodyForce = {0, 0, -9.81}
}

Problem.Solver.HeatEq = {

    -- Enable the fluid-structure interface

    BC = {FSITExt = true},

    -- Define the solver algorithms

    nlAlgo = 'Picard',
    timeIntegration = 'BackwardEuler',
    residual = 'Ax_f',

    -- Other simulation parameters

    maxIter = 25,
    minRes = 1e-6,
    tolerance = 1e-16,
}

-- Initial Conditions

function Problem.Solver.IC.initStates(x, y, z)
	return {0, 0, 0, 0, 340}
end

-- Momentum Continuity Equation BC

function Problem.Solver.MomContEq.BC.TopV(x, y, z, t)
	return 0, 0, 0
end

function Problem.Solver.MomContEq.BC.BottomV(x, y, z, t)
	return 0, 0, 0
end

-- Heat Equation BC

function Problem.Solver.HeatEq.BC.TopQ(x, y, z, t)
    return 0, 0, 0
end

function Problem.Solver.HeatEq.BC.BottomQ(x, y, z, t)
    return 0, 0, 0
end

function Problem.Solver.HeatEq.BC.FreeSurfaceQ(x, y, z, t)
    return 0, 0, 0
end

-- Characteristic Size

function Problem.Mesh.computeHcharFromDistance(x, y, z, t, dist)
    return Problem.Mesh.hchar+dist*0.05
end