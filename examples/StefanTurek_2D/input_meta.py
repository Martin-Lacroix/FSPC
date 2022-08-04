import toolbox.gmsh as gmsh
import wrap as w
import os

# %% Parallel Computing

metafor = None
w.StrVectorBase.useTBB()
w.StrMatrixBase.useTBB()
w.ContactInteraction.useTBB()

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
    solvermanager = metafor.getSolverManager()
    interactionset = domain.getInteractionSet()
    mim = metafor.getMechanicalIterationManager()

    # Plane strain and DSS solver

    domain.getGeometry().setDimPlaneStrain(1)
    solvermanager.setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__),'geometry.msh')
    importer = gmsh.GmshImport(mshFile,domain)
    groups = importer.groups
    importer.verb = False
    importer.execute()

    # Defines the solid domain

    app1 = w.FieldApplicator(1)
    app1.push(groups['Solid'])
    interactionset.add(app1)

    app2 = w.FieldApplicator(2)
    app2.push(groups['Solid'])
    interactionset.add(app2)

    # Solid material parameters

    materset.define(1,w.ElastHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS,1.4e6) # 5.6e6 for Turek
    materset(1).put(w.POISSON_RATIO,0.4)
    materset(1).put(w.MASS_DENSITY,1e3)

    # Finite element properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp1.put(w.MATERIAL,1)
    app1.addProperty(prp1)

    prp2 = w.ElementProperties(w.TriangleVolume2DElement)
    prp2.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp2.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp2.put(w.MATERIAL,1)
    app2.addProperty(prp2)

    # Boundary conditions
    
    loadingset.define(groups['Clamped'],w.Field1D(w.TX,w.RE))
    loadingset.define(groups['Clamped'],w.Field1D(w.TY,w.RE))

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

    input['FSInterface'] = groups['FSInterface']
    input['exporter'] = gmsh.GmshExport('metafor/solid.msh',metafor)
    input['exporter'].addInternalField([w.IF_EVMS,w.IF_P])
    return metafor