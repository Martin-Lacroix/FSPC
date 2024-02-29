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
    domain.getGeometry().setDimPlaneStrain(1)
    metafor.getSolverManager().setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__),'geometryS.msh')
    importer = gmsh.GmshImport(mshFile,domain)
    groups = importer.groups
    importer.execute()
    
    # Defines the solid domain

    iset = domain.getInteractionSet()
    app1 = w.FieldApplicator(1)
    app1.push(groups['Peigne'])
    iset.add(app1)

    app2 = w.FieldApplicator(2)
    app2.push(groups['Disk'])
    iset.add(app2)
    
    # Wall material parameters

    E = 200
    v = 0.3
    G = E/(2*(1+v))
    K = E/(3*(1-2*v))

    materset = domain.getMaterialSet()
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
    load1 = w.NodInteraction(3)
    load1.push(groups['PeigneSide'])
    load1.push(groups['Clamped'])
    load1.addProperty(prp3)
    iset.add(load1)

    prp4 = w.ElementProperties(w.NodStress2DElement)
    load2 = w.NodInteraction(4)
    load2.push(groups['DiskSide'])
    load2.addProperty(prp4)
    iset.add(load2)

    # Contact properties

    prp5 = w.ElementProperties(w.Contact2DElement)
    prp5.put(w.AREAINCONTACT,w.AIC_ONCE)
    prp5.put(w.MATERIAL,3)

    # Defines the contact entities

    ci = w.DdContactInteraction(5)
    ci.setTool(groups['PeigneSide'])
    ci.setSmoothNormals(False)
    ci.push(groups['DiskSide'])
    ci.setSinglePass()
    ci.addProperty(prp5)
    iset.add(ci)

    # Boundary conditions

    loadingset = domain.getLoadingSet()
    loadingset.define(groups['Clamped'],w.Field1D(w.TX,w.RE))
    loadingset.define(groups['Clamped'],w.Field1D(w.TY,w.RE))

    # Mechanical time integration

    ti = w.AlphaGeneralizedTimeIntegration(metafor)
    metafor.setTimeIntegration(ti)

    # Mechanical iterations

    mim = metafor.getMechanicalIterationManager()
    mim.setResidualTolerance(1e-4)
    mim.setMaxNbOfIterations(25)

    # Time step iterations
    
    tsm = metafor.getTimeStepManager()
    tscm = w.NbOfMechNRIterationsTimeStepComputationMethod(metafor)
    tsm.setTimeStepComputationMethod(tscm)
    tscm.setTimeStepDivisionFactor(2)
    tscm.setNbOptiIte(25)

    # Parameters for FSPC

    parm['interacM'] = [load1,load2]
    parm['FSInterface'] = groups['FSInterface']
    parm['exporter'] = gmsh.NodalGmshExport('metafor/output.msh',metafor)
    parm['polytope'] = load1.getElementSet()

    extr = w.IFNodalValueExtractor(groups['Peigne'],w.IF_EVMS)
    parm['exporter'].addExtractor(extr)

    extr = w.IFNodalValueExtractor(groups['Disk'],w.IF_EVMS)
    parm['exporter'].addExtractor(extr)
    
    domain.build()
    return metafor