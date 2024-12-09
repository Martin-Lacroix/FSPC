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

    remeshAlgo = 'CGAL_Edge',
    mshFile = 'geometry_F.msh',
    deleteBoundElements = {'FSInterface'},
    localHcharGroups = {'FSInterface'},
    boundingBox = {-5, -5, 5, 5},
    exclusionZones = {},

    -- Remeshing internal parameters

    alpha = 1.2,
    omega = 1.0,
    gamma = 0.3,
    hchar = 0.1,
    gammaFS = 0.2,
    gammaEdge = 0.2,
    minHeightFactor = 1e-3,

    -- Enable or disable algorithms

    addOnFS = false,
    keepFluidElements = true,
    deleteFlyingNodes = false
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
        mu = 0.71
    },
    
    -- Parameters for the fluid bulk

    StateEquation = {
        type = 'Incompressible_LinearT',
        alphaLin = 0.071,
        Tr = 1e3,
        rho = 1
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
        Tr = 1e3,
        cp = 1
    },

    -- Parameters for Fourier flux

    HeatFlux = {
        type = 'LinearFourierFlux',
        DkDT = 0,
        Tr = 1e3,
        k = 1
    },

    -- Parameters for cooling law
    
    CoolingLaw = {
        type = 'LinearCoolingLaw',
        Tinf = 1e3,
        h = 0
    },

    -- Parameters for optical material
    
    OpticalProperties = {
        type = 'ConstantOpticalProperties',
        absorptivity = 0,
        emissivity = 0,
        sigmaSB = 0,
        Tinf = 1e3
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

    -- Enable the boundary conditions

    BC = {},

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
    bodyForce = {0, -10}
}

Problem.Solver.HeatEq = {

    -- Enable the fluid-structure interface

    BC = {FSInterfaceTExt = true},

    -- Define the solver algorithms

    nlAlgo = 'Picard',
    timeIntegration = 'BackwardEuler',
    residual = 'Ax_f',

    -- Other simulation parameters

    maxIter = 25,
    minRes = 1e-6,
    tolerance = 1e-16
}

-- Initial Conditions

function Problem.Solver.IC.initStates(x, y, z)
	return {0, 0, 0, 1000}
end

-- Momentum Continuity Equation BC

function Problem.Solver.MomContEq.BC.WallV(x, y, z, t)
	return 0, 0
end

function Problem.Solver.MomContEq.BC.FSInterfaceV(x, y, z, t)
	return 0, 0
end

-- Heat Equation BC

function Problem.Solver.HeatEq.BC.WallQ(x, y, z, t)
    return 0, 0
end

function Problem.Solver.HeatEq.BC.FreeSurfaceQ(x, y, z, t)
    return 0, 0
end

-- Characteristic Size

function Problem.Mesh.computeHcharFromDistance(x, y, z, t, dist)
	return Problem.Mesh.hchar+dist*0.1
end
