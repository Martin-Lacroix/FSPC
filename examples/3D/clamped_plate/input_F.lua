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
    localHcharGroups = {'FSI'},
    boundingBox = {-0.2, -0.2, 0, 0.2, 0.2, 0.64},
    exclusionZones = {},

    -- Remeshing internal parameters

    alpha = 1.2,
    omega = 0.5,
    gamma = 0.6,
    hchar = 0.01,
    gammaFS = 0.6,
    gammaEdge = 0.2,
    minHeightFactor = 1e-3,

    -- Enable or disable algorithms

    addOnFS = true,
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
        mu = 1e-3
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
    minRes = 1e-8,
    tolerance = 1e-16,
    bodyForce = {0, 0, -9.81}
}

-- Initial Conditions

function Problem.Solver.IC.initStates(x, y, z)
	return {0, 0, 0, 0}
end

-- Momentum Continuity Equation BC

function Problem.Solver.MomContEq.BC.WallV(x, y, z, t)
	return 0, 0, 0
end

-- Characteristic Size

function Problem.Mesh.computeHcharFromDistance(x, y, z, t, dist)
	return Problem.Mesh.hchar+dist*0.05
end
