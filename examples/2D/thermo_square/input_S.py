import toolbox.gmsh as gmsh
import wrap as w
import os

metafor = None
def getMetafor(parm):
    '''
    Initialize and return the metafor object
    '''

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

    parm['FSI'] = groups['FSI']

    # Defines the ball domain

    iset = domain.getInteractionSet()
    app = w.FieldApplicator(1)
    app.push(groups['Solid'])
    iset.add(app)

    # Solid material parameters

    materset = domain.getMaterialSet()
    materset.define(1, w.TmElastHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS, 1)
    materset(1).put(w.THERM_EXPANSION, 0)
    materset(1).put(w.HEAT_CAPACITY, 1)
    materset(1).put(w.MASS_DENSITY, 10)
    materset(1).put(w.POISSON_RATIO, 0)
    materset(1).put(w.CONDUCTIVITY, 1)
    materset(1).put(w.DISSIP_TE, 0)
    materset(1).put(w.DISSIP_TQ, 0)

    # Finite element properties

    prp1 = w.ElementProperties(w.TmVolume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH, w.VES_CMVIM_SRIPR)
    prp1.put(w.STIFFMETHOD, w.STIFF_ANALYTIC)
    prp1.put(w.MATERIAL, 1)
    app.addProperty(prp1)

    # Elements for surface heat flux

    prp2 = w.ElementProperties(w.NodHeatFlux2DElement)
    heat = w.NodInteraction(2)
    heat.push(groups['FSI'])
    heat.addProperty(prp2)
    iset.add(heat)

    parm['interaction_T'] = heat

    # Boundary conditions

    initset = domain.getInitialConditionSet()
    initset.define(groups['Solid'], w.Field1D(w.TO, w.AB), 2e3)

    loadset = domain.getLoadingSet()
    loadset.define(groups['Solid'], w.Field1D(w.TX, w.RE))
    loadset.define(groups['Solid'], w.Field1D(w.TY, w.RE))

    # Mechanical and thermal time integration

    ti_M = w.QuasiStaticTimeIntegration(metafor)
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

    # Nodal Gmsh exporter

    ext = w.GmshExporter(metafor, 'metafor/output')
    ext.add(w.DbNodalValueExtractor(groups['Solid'], w.Field1D(w.TO, w.RE)))
    ext.add(w.DbNodalValueExtractor(groups['Solid'], w.Field1D(w.TO, w.AB)))
    parm['exporter'] = ext

    # Build domain and folder

    domain.build()
    os.makedirs('metafor')
    return metafor