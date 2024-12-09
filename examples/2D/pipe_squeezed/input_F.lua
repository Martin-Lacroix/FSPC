Problem = {

    -- Main simulation parameters

    mechanical = true,
    verboseOutput = true,
    autoRemeshing = false,
    simulationTime = math.huge
}

Problem.Mesh = {

    -- Input mesh and bounding box

    remeshAlgo = 'CGAL_Edge',
    mshFile = 'geometry_F.msh',
    deleteBoundElements = {'FSI'},
    boundingBox = {-1, -2.625, 1, 2.375},
    exclusionZones = {},

    -- Remeshing internal parameters

    alpha = 1.2,
    omega = 0.5,
    gamma = 0.3,
    hchar = 0.04,
    gammaFS = 0.2,
    gammaEdge = 0.2,
    minHeightFactor = 1e-3,

    -- Enable or disable algorithms

    addOnFS = true,
    keepFluidElements = false,
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
        type = 'TaitMurnaghan',
        rho0 = 1e-6,
        K0 = 100,
        K0p = 1,
        p0 = 0
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
    type = 'Explicit',
    timeIntegration = 'CDS',

    -- Factors of time step changes

    securityCoeff = 0.2,

    -- Enable or disable algorithms

    adaptDT = true,
    maxDT = math.huge,
    initialDT = math.huge
}

Problem.Solver.MomEq = {

    -- Enable the fluid-structure interface

    BC = {FSIVExt = true},

    -- Other simulation parameters

    pExt = 0,
    bodyForce = {0, 0}
}

Problem.Solver.ContEq = {

    -- Enable the boundary conditions

    BC = {},

    -- Define the solver algorithms

    version = 'DpDt',
    stabilization = 'CLS'
}

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
