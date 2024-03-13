import toolbox.gmsh as gmsh
import wrap as w
import os

# |------------------------------------------|
# |   Initialization and Input Parameters    |
# |------------------------------------------|

metafor = None
def getMetafor(parm):

    global metafor
    if metafor: return metafor
    metafor = w.Metafor()

    w.StrVectorBase.useTBB()
    w.StrMatrixBase.useTBB()
    w.ContactInteraction.useTBB()

    # Dimension and DSS solver

    domain = metafor.getDomain()
    domain.getGeometry().setDimPlaneStrain(1)
    metafor.getSolverManager().setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__), 'geometry_S.msh')
    importer = gmsh.GmshImport(mshFile, domain)
    groups = importer.groups
    importer.execute()

    # Defines the solid domain

    iset = domain.getInteractionSet()
    app = w.FieldApplicator(1)
    app.push(groups['S1'])
    app.push(groups['S2'])
    app.push(groups['S3'])
    iset.add(app)

    # Solid material parameters

    materset = domain.getMaterialSet()
    materset.define(1, w.TmElastHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS, 1e7)
    materset(1).put(w.THERM_EXPANSION, 0)
    materset(1).put(w.HEAT_CAPACITY, 100)
    materset(1).put(w.MASS_DENSITY, 950)
    materset(1).put(w.POISSON_RATIO, 0)
    materset(1).put(w.CONDUCTIVITY, 5)
    materset(1).put(w.DISSIP_TE, 0)
    materset(1).put(w.DISSIP_TQ, 0)

    # Finite element properties

    prp1 = w.ElementProperties(w.TmVolume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH, w.VES_CMVIM_SRIPR)
    prp1.put(w.STIFFMETHOD, w.STIFF_ANALYTIC)
    prp1.put(w.GRAVITY_Y, -9.81)
    prp1.put(w.MATERIAL, 1)
    app.addProperty(prp1)

    # Elements for surface heat flux

    prp2 = w.ElementProperties(w.NodHeatFlux2DElement)
    heat = w.NodInteraction(2)
    heat.push(groups['FSInterface'])
    heat.addProperty(prp2)
    iset.add(heat)

    # Elements for surface traction

    prp3 = w.ElementProperties(w.NodStress2DElement)
    load = w.NodInteraction(3)
    load.push(groups['FSInterface'])
    load.addProperty(prp3)
    iset.add(load)

    parm['interaction_T'] = heat
    parm['interaction_M'] = load
    parm['polytope'] = load.getElementSet()

    # Initial and boundary conditions

    initset = metafor.getInitialConditionSet()
    initset.define(groups['S1'], w.Field1D(w.TO, w.AB), 180)
    initset.define(groups['S2'], w.Field1D(w.TO, w.AB), 200)
    initset.define(groups['S3'], w.Field1D(w.TO, w.AB), 220)

    # Mechanical and thermal time integration

    ti_M = w.AlphaGeneralizedTimeIntegration(metafor)
    ti_T = w.TrapezoidalThermalTimeIntegration(metafor)

    ti = w.StaggeredTmTimeIntegration(metafor)
    ti.setMechanicalTimeIntegration(ti_M)
    ti.setThermalTimeIntegration(ti_T) 
    metafor.setTimeIntegration(ti)

    # Mechanical and thermal iterations

    mim = metafor.getMechanicalIterationManager()
    mim.setResidualTolerance(1e-6)
    mim.setMaxNbOfIterations(25)

    tim = metafor.getThermalIterationManager()
    tim.setResidualTolerance(1e-6)
    tim.setMaxNbOfIterations(25)

    # Time step iterations
    
    tsm = metafor.getTimeStepManager()
    tscm = w.NbOfStaggeredTmNRIterationsTimeStepComputationMethod(metafor)
    tsm.setTimeStepComputationMethod(tscm)
    tscm.setTimeStepDivisionFactor(2)
    tscm.setNbOptiIte(25)

    # Nodal GMSH extractor

    ext = w.GmshNodalExtractor(metafor, 'metafor/output')
    ext.add(1, w.DbNodalValueExtractor(groups['Solid'], w.Field1D(w.TO, w.AB)))
    ext.add(2, w.DbNodalValueExtractor(groups['Solid'], w.Field1D(w.TO, w.RE)))
    parm['extractor'] = ext

    # Build domain and folder

    domain.build()
    parm['FSInterface'] = groups['FSInterface']
    os.makedirs('metafor')
    return metafor