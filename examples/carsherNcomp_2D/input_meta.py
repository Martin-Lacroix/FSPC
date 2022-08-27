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
    lawset = domain.getMaterialLawSet()
    loadingset = domain.getLoadingSet()
    solvermanager = metafor.getSolverManager()
    interactionset = domain.getInteractionSet()
    mim = metafor.getMechanicalIterationManager()

    # Dimension and DSS solver

    domain.getGeometry().setDimPlaneStrain(1)
    solvermanager.setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__),'geometry.msh')
    importer = gmsh.GmshImport(mshFile,domain)
    importer.verb = importer.writeLogs = False
    groups = importer.groups
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
    materset(2).put(w.PROF_CONT,0.005)

    # Volume solid properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp1.put(w.GRAVITY_Y,-9.81)
    prp1.put(w.MATERIAL,1)
    app.addProperty(prp1)

    # Contact properties

    prp2 = w.ElementProperties(w.Contact2DElement)
    prp2.put(w.AREAINCONTACT,w.AIC_ONCE)
    prp2.put(w.MATERIAL,2)

    # Contact for PolyTop and Solid

    ci1 = w.RdContactInteraction(2)
    ci1.setTool(groups['PolyTop'])
    ci1.setSmoothNormals(False)
    ci1.push(groups['Solid'])
    ci1.addProperty(prp2)
    interactionset.add(ci1)

    # Contact for PolyTop and Solid

    ci2 = w.RdContactInteraction(3)
    ci2.setTool(groups['PolyBot'])
    ci2.setSmoothNormals(False)
    ci2.push(groups['Solid'])
    ci2.addProperty(prp2)
    interactionset.add(ci2)

    # Boundary conditions

    loadingset.define(groups['PolyTop'],w.Field1D(w.TX,w.RE))
    loadingset.define(groups['PolyTop'],w.Field1D(w.TY,w.RE))
    loadingset.define(groups['PolyBot'],w.Field1D(w.TX,w.RE))
    loadingset.define(groups['PolyBot'],w.Field1D(w.TY,w.RE))

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