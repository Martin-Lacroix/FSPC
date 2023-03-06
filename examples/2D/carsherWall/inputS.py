import toolbox.gmsh as gmsh
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
    lawset = domain.getMaterialLawSet()
    loadingset = domain.getLoadingSet()
    solvermanager = metafor.getSolverManager()
    interactionset = domain.getInteractionSet()
    mim = metafor.getMechanicalIterationManager()

    # Dimension and DSS solver

    domain.getGeometry().setDimPlaneStrain(1)
    solvermanager.setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__),'geometryS.msh')
    importer = gmsh.GmshImport(mshFile,domain)
    groups = importer.groups
    importer.binary = True
    importer.execute()
    
    # Defines the solid domain

    app = w.FieldApplicator(1)
    app.push(groups['Solid'])
    interactionset.add(app)
    
    # Solid material parameters

    materset.define(1,w.EvpIsoHHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS,1e7)
    materset(1).put(w.MASS_DENSITY,8e3)
    materset(1).put(w.POISSON_RATIO,0)
    materset(1).put(w.YIELD_NUM,1)

    lawset.define(1,w.SwiftIsotropicHardening)
    lawset(1).put(w.IH_SIGEL,1e5)
    lawset(1).put(w.IH_B,375)
    lawset(1).put(w.IH_N,0.2)

    # Contact parameters

    materset.define(2,w.CoulombContactMaterial)
    materset(2).put(w.COEF_FROT_DYN,0.15)
    materset(2).put(w.COEF_FROT_STA,0.15)
    materset(2).put(w.PEN_NORMALE,1e8)
    materset(2).put(w.PEN_TANGENT,1e8)
    materset(2).put(w.PROF_CONT,0.01)

    # Volume solid properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp1.put(w.GRAVITY_Y,-9.81)
    prp1.put(w.MATERIAL,1)
    app.addProperty(prp1)

    # Elements for surface traction

    prp2 = w.ElementProperties(w.NodStress2DElement)
    load = w.NodInteraction(2)
    load.push(groups['FSInterface'])
    load.addProperty(prp2)
    interactionset.add(load)

    # Contact properties

    prp3 = w.ElementProperties(w.Contact2DElement)
    prp3.put(w.AREAINCONTACT,w.AIC_ONCE)
    prp3.put(w.MATERIAL,2)

    # Contact for Tool and Solid

    ci = w.RdContactInteraction(3)
    ci.setTool(groups['Contact'])
    ci.setSmoothNormals(False)
    ci.push(groups['Solid'])
    ci.addProperty(prp3)
    interactionset.add(ci)

    # Boundary conditions

    loadingset.define(groups['Contact'],w.Field1D(w.TX,w.RE))
    loadingset.define(groups['Contact'],w.Field1D(w.TY,w.RE))

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
    input['exporter'] = gmsh.GmshExport('metafor/output.msh',metafor)
    input['exporter'].addInternalField([w.IF_EVMS,w.IF_P])
    input['exporter'].binary = True
    return metafor