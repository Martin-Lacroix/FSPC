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

    domain.getGeometry().setDim3D()
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
    materset(1).put(w.ELASTIC_MODULUS,1.23e6)
    materset(1).put(w.POISSON_RATIO,0.3)
    materset(1).put(w.MASS_DENSITY,1030)

    # Finite element properties

    prp1 = w.ElementProperties(w.Volume3DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp1.put(w.MATERIAL,1)
    app.addProperty(prp1)

    # Elements for surface traction

    prp2 = w.ElementProperties(w.NodTraction3DElement)
    load = w.NodLoadingInteraction(2)
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

    input['interaction'] = load
    input['FSInterface'] = groups['FSInterface']
    input['exporter'] = meshio.MeshioExport('metafor/solid.msh',metafor)
    input['exporter'].addInternalField([w.IF_EVMS,w.IF_P])
    input['exporter'].format = 'gmsh'
    return metafor