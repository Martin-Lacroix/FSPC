import toolbox.gmsh as gmsh
import wrap as w
import os

# |-----------------------------------------|
# |   Initialization and Input Parameters   |
# |-----------------------------------------|

metafor = None
def getMetafor(parm):

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
    importer = gmsh.GmshImport(mshFile,domain)
    groups = importer.groups
    importer.execute()
    
    # Defines the solid domain

    app1 = w.FieldApplicator(1)
    app1.push(groups['Border'])
    interactionset.add(app1)

    # Defines the ball domain

    app2 = w.FieldApplicator(2)
    app2.push(groups['Ball'])
    interactionset.add(app2)
    
    # Wall material parameters

    E = 200
    v = 0.3
    G = E/(2*(1+v))
    K = E/(3*(1-2*v))

    materset.define(1,w.NeoHookeanHyperPk2Material)
    materset(1).put(w.MASS_DENSITY,1e-6)
    materset(1).put(w.HYPER_K0,K)
    materset(1).put(w.HYPER_G0,G)

    # Ball material parameters

    E = 100
    v = 0.3
    G = E/(2*(1+v))
    K = E/(3*(1-2*v))

    materset.define(2,w.NeoHookeanHyperPk2Material)
    materset(2).put(w.MASS_DENSITY,1e-6)
    materset(2).put(w.HYPER_K0,K)
    materset(2).put(w.HYPER_G0,G)

    # Contact parameters

    penalty = 1e4
    friction = 0.15

    materset.define(3,w.CoulombContactMaterial)
    materset(3).put(w.PEN_TANGENT,friction*penalty)
    materset(3).put(w.COEF_FROT_DYN,friction)
    materset(3).put(w.COEF_FROT_STA,friction)
    materset(3).put(w.PEN_NORMALE,penalty)
    materset(3).put(w.PROF_CONT,0.1)
    
    # Volume solid properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp1.put(w.MATERIAL,1)
    app1.addProperty(prp1)

    # Volume ball properties

    prp2 = w.ElementProperties(w.Volume2DElement)
    prp2.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp2.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp2.put(w.MATERIAL,2)
    app2.addProperty(prp2)

    # Elements for surface traction

    prp3 = w.ElementProperties(w.NodStress2DElement)
    load = w.NodInteraction(3)
    load.push(groups['FSInterface'])
    load.addProperty(prp3)
    interactionset.add(load)

    # Contact properties

    prp4 = w.ElementProperties(w.Contact2DElement)
    prp4.put(w.AREAINCONTACT,w.AIC_ONCE)
    prp4.put(w.MATERIAL,3)

    # Defines the contact entities

    ci = w.DdContactInteraction(4)
    ci.setTool(groups['Master'])
    ci.setSmoothNormals(False)
    ci.push(groups['Slave'])
    ci.setSinglePass()
    ci.addProperty(prp4)
    interactionset.add(ci)

    # Boundary conditions

    loadingset.define(groups['Clamped'],w.Field1D(w.TX,w.RE))
    loadingset.define(groups['Clamped'],w.Field1D(w.TY,w.RE))

    # Mechanical time integration

    ti = w.AlphaGeneralizedTimeIntegration(metafor)
    metafor.setTimeIntegration(ti)

    # Mechanical iterations

    mim.setMaxNbOfIterations(25)
    mim.setResidualTolerance(1e-4)

    # Time step iterations
    
    tscm = w.NbOfMechNRIterationsTimeStepComputationMethod(metafor)
    tsm.setTimeStepComputationMethod(tscm)
    tscm.setTimeStepDivisionFactor(2)
    tscm.setNbOptiIte(25)

    # Parameters for FSPC

    parm['interacM'] = load
    parm['FSInterface'] = groups['FSInterface']
    parm['exporter'] = gmsh.GmshExport('metafor/output.msh',metafor)
    parm['exporter'].addInternalField([w.IF_EVMS,w.IF_P])
    return metafor