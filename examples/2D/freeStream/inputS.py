import toolbox.meshio as meshio
import wrap as w
import os

# %% Main Function

metafor = None
def getMetafor(input):

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

    domain.getGeometry().setDimPlaneStrain(1)
    solvermanager.setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__),'geometryS.msh')
    importer = meshio.MeshioImport(mshFile,metafor)
    groups = importer.groups
    importer.execute()

    # Defines the solid domain
    
    app = w.FieldApplicator(1)
    app.push(groups['Solid'])
    interactionset.add(app)

    # Material parameters

    materset.define(1,w.ElastHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS,1e9)
    materset(1).put(w.POISSON_RATIO,0.3)
    materset(1).put(w.MASS_DENSITY,8e3)

    # Finite element properties

    prp = w.ElementProperties(w.TriangleVolume2DElement)
    prp.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp.put(w.MATERIAL,1)
    app.addProperty(prp)

    # Elements for surface traction

    prp2 = w.ElementProperties(w.NodTraction2DElement)
    load = w.NodInteraction(2)
    load.push(groups['FSInterface'])
    load.addProperty(prp2)
    interactionset.add(load)

    # Boundary conditions

    loadingset.define(groups['SolidBase'],w.Field1D(w.TX,w.RE))
    loadingset.define(groups['SolidBase'],w.Field1D(w.TY,w.RE))


    #loadingset.define(groups['Solid'],w.Field1D(w.TX,w.RE))
    #loadingset.define(groups['Solid'],w.Field1D(w.TY,w.RE))

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

    input['interacM'] = load
    input['FSInterface'] = groups['FSInterface']
    input['exporter'] = meshio.MeshioExport('metafor/solid.msh',metafor)
    input['exporter'].addInternalField([w.IF_EVMS,w.IF_P])
    input['exporter'].format = 'gmsh'
    return metafor