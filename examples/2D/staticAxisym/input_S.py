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
    domain.getGeometry().setDimAxisymmetric()
    metafor.getSolverManager().setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__), 'geometry_S.msh')
    importer = gmsh.GmshImport(mshFile, domain)
    groups = importer.groups
    importer.execute()

    # Defines the ball domain

    iset = domain.getInteractionSet()
    app = w.FieldApplicator(1)
    app.push(groups['Solid'])
    iset.add(app)

    # Solid material parameters

    materset = domain.getMaterialSet()
    materset.define(1, w.ElastHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS, 1e7)
    materset(1).put(w.MASS_DENSITY, 8e3)
    materset(1).put(w.POISSON_RATIO, 0)

    # Finite element properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH, w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD, w.STIFF_ANALYTIC)
    prp1.put(w.MATERIAL, 1)
    app.addProperty(prp1)

    parm['interaction_M'] = load

    # Elements for surface traction

    prp2 = w.ElementProperties(w.NodStress2DElement)
    load = w.NodInteraction(2)
    load.push(groups['FSInterface'])
    load.addProperty(prp2)
    iset.add(load)

    # Boundary conditions
    
    loadset = domain.getLoadingSet()
    loadset.define(groups['Clamped'], w.Field1D(w.TX, w.RE))
    loadset.define(groups['Clamped'], w.Field1D(w.TY, w.RE))
    loadset.define(groups['Axis'], w.Field1D(w.TX, w.RE))

    # Mechanical time integration

    ti = w.AlphaGeneralizedTimeIntegration(metafor)
    metafor.setTimeIntegration(ti)

    # Mechanical iterations

    mim = metafor.getMechanicalIterationManager()
    mim.setResidualTolerance(1e-8)
    mim.setMaxNbOfIterations(25)

    # Time step iterations
    
    tsm = metafor.getTimeStepManager()
    tscm = w.NbOfMechNRIterationsTimeStepComputationMethod(metafor)
    tsm.setTimeStepComputationMethod(tscm)
    tscm.setTimeStepDivisionFactor(2)
    tscm.setNbOptiIte(25)

    # Nodal GMSH extractor

    ext = w.GmshNodalExtractor(metafor, 'metafor/output')
    ext.add(1, w.IFNodalValueExtractor(groups['Solid'], w.IF_P))
    ext.add(2, w.IFNodalValueExtractor(groups['Solid'], w.IF_EVMS))
    parm['extractor'] = ext

    # Build domain and folder

    domain.build()
    parm['FSInterface'] = groups['FSInterface']
    os.makedirs('metafor')
    return metafor