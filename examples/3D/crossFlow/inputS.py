import toolbox.gmsh as gmsh
import wrap as w
import os

# %% Main Function

metafor = None
def getMetafor(param):

    global metafor
    if metafor: return metafor

    w.StrVectorBase.useTBB()
    w.StrMatrixBase.useTBB()
    w.ContactInteraction.useTBB()
    
    # Group and interaction sets

    metafor = w.Metafor()
    domain = metafor.getDomain()
    tsm = metafor.getTimeStepManager()
    materset = domain.getMaterialSet()
    loadingset = domain.getLoadingSet()
    solvermanager = metafor.getSolverManager()
    interactionset = domain.getInteractionSet()
    mim = metafor.getMechanicalIterationManager()

    # Dimension and DSS solver

    domain.getGeometry().setDim3D()
    solvermanager.setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__),'geometryS.msh')
    importer = gmsh.GmshImport(mshFile,domain)
    groups = importer.groups
    importer.execute()

    # Defines the solid domain

    app = w.FieldApplicator(1)
    app.push(groups['Solid'])
    interactionset.add(app)

    # Material parameters

    materset.define(1,w.ElastHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS,1.23e6)
    materset(1).put(w.POISSON_RATIO,0.3)
    materset(1).put(w.MASS_DENSITY,1030)
    
    # Finite element properties

    prp = w.ElementProperties(w.Volume3DElement)
    prp.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_EAS)
    prp.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp.put(w.TOTAL_LAGRANGIAN,True)
    prp.put(w.GRAVITY_Z,-9.81)
    prp.put(w.MATERIAL,1)
    prp.put(w.PEAS,1e-9)
    app.addProperty(prp)

    # Elements for surface traction

    prp2 = w.ElementProperties(w.NodStress3DElement)
    load = w.NodInteraction(2)
    load.push(groups['FSInterface'])
    load.addProperty(prp2)
    interactionset.add(load)
    
    # Boundary conditions
    
    loadingset.define(groups['Clamped'],w.Field1D(w.TX,w.RE))
    loadingset.define(groups['Clamped'],w.Field1D(w.TY,w.RE))
    loadingset.define(groups['Clamped'],w.Field1D(w.TZ,w.RE))

    # Mechanical time integration

    ti = w.AlphaGeneralizedTimeIntegration(metafor)
    metafor.setTimeIntegration(ti)

    # Mechanical iterations

    mim.setMaxNbOfIterations(25)
    mim.setResidualTolerance(1e-6)

    # Time step iterations

    tscm = w.NbOfMechNRIterationsTimeStepComputationMethod(metafor)
    tsm.setTimeStepComputationMethod(tscm)
    tscm.setTimeStepDivisionFactor(2)
    tscm.setNbOptiIte(25)

    # Parameters for FSPC

    param['interacM'] = load
    param['FSInterface'] = groups['FSInterface']
    param['exporter'] = gmsh.GmshExport('metafor/output.msh',metafor)
    param['exporter'].addInternalField([w.IF_EVMS,w.IF_P])
    return metafor