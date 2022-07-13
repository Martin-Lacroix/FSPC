import toolbox.gmsh as gmsh
import wrap as w
import os

# %% Parallel Computing

metafor = None
# w.StrVectorBase.useTBB()
# w.StrMatrixBase.useTBB()
# w.ContactInteraction.useTBB()

# %% Main Function

def getMetafor(input):

    global metafor
    if metafor: return metafor
    
    # Group and interaction sets

    metafor = w.Metafor()
    domain = metafor.getDomain()
    tsm = metafor.getTimeStepManager()
    materset = domain.getMaterialSet()
    loadingset = domain.getLoadingSet()
    #solvermanager = metafor.getSolverManager()
    interactionset = domain.getInteractionSet()
    mim = metafor.getMechanicalIterationManager()

    # Dimension and DSS solver

    domain.getGeometry().setDim3D()
    #solvermanager.setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__),'geometry.msh')
    importer = gmsh.GmshImport(mshFile,domain)
    importer.writeLogs = False
    groups = importer.groups
    importer.execute()

    # Defines the solid domain

    app = w.FieldApplicator(1)
    app.push(groups['Solid'])
    interactionset.add(app)
    
    # Material parameters

    # G = 2.4e6
    # C1 = -1.2e6
    # C2 = G/2.0-C1

    # materset.define(1,w.MooneyRivlinHyperMaterial)
    # materset(1).put(w.RUBBER_PENAL,1.3e6)
    # materset(1).put(w.MASS_DENSITY,1100)
    # materset(1).put(w.RUBBER_C1,C1)
    # materset(1).put(w.RUBBER_C2,C2)


    materset.define(1,w.ElastHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS,1e7)
    materset(1).put(w.MASS_DENSITY,1100)
    materset(1).put(w.POISSON_RATIO,0.4)
    
    # Finite element properties

    prp = w.ElementProperties(w.TetraVolume3DElement)
    prp.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp.put(w.GRAVITY_Y,-9.81)
    prp.put(w.MATERIAL,1)
    app.addProperty(prp)

    # prp = w.ElementProperties(w.TetraVolume3DElement)
    # prp.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    # prp.put(w.STIFFMETHOD,w.STIFF_NUMERIC)
    # prp.put(w.GRAVITY_Y,-9.81)
    # prp.put(w.MATERIAL,1)
    # app.addProperty(prp)
    
    # Boundary conditions
    
    loadingset.define(groups['SolidBase'],w.Field1D(w.TX,w.RE))
    loadingset.define(groups['SolidBase'],w.Field1D(w.TY,w.RE))
    loadingset.define(groups['SolidBase'],w.Field1D(w.TZ,w.RE))
    loadingset.define(groups['SolidSide'],w.Field1D(w.TY,w.RE))

    # Mechanical time integration

    ti = w.AlphaGeneralizedTimeIntegration(metafor)
    metafor.setTimeIntegration(ti)

    # Mechanical iterations

    mim.setMaxNbOfIterations(25)
    mim.setResidualTolerance(1e-7)

    # Time step iterations

    tscm = w.NbOfMechNRIterationsTimeStepComputationMethod(metafor)
    tsm.setTimeStepComputationMethod(tscm)
    tscm.setTimeStepDivisionFactor(2)
    tscm.setNbOptiIte(25)

    # Parameters for FSPC

    input['FSInterface'] = groups['FSInterface']
    input['exporter'] = gmsh.GmshExport('metafor/solid.msh',metafor)
    input['exporter'].addInternalField([w.IF_EVMS,w.IF_P])
    return metafor