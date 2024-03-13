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

    mshFile = os.path.join(os.path.dirname(__file__), 'geometry_S.msh')
    importer = gmsh.GmshImport(mshFile, domain)
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
    G = E/(2*(1 + v))
    K = E/(3*(1-2*v))

    materset = domain.getMaterialSet()
    materset.define(1, w.NeoHookeanHyperPk2Material)
    materset(1).put(w.MASS_DENSITY, 1e-6)
    materset(1).put(w.HYPER_K0, K)
    materset(1).put(w.HYPER_G0, G)

    # Ball material parameters

    E = 100
    v = 0.3
    G = E/(2*(1 + v))
    K = E/(3*(1-2*v))

    materset.define(2, w.NeoHookeanHyperPk2Material)
    materset(2).put(w.MASS_DENSITY, 1e-6)
    materset(2).put(w.HYPER_K0, K)
    materset(2).put(w.HYPER_G0, G)

    # Contact parameters

    penalty = 1e4
    friction = 0.15

    materset.define(3, w.CoulombContactMaterial)
    materset(3).put(w.PEN_TANGENT, friction*penalty)
    materset(3).put(w.COEF_FROT_DYN, friction)
    materset(3).put(w.COEF_FROT_STA, friction)
    materset(3).put(w.PEN_NORMALE, penalty)
    materset(3).put(w.PROF_CONT, 0.1)
    
    # Volume solid properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH, w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD, w.STIFF_ANALYTIC)
    prp1.put(w.MATERIAL, 1)
    app1.addProperty(prp1)

    # Volume ball properties

    prp2 = w.ElementProperties(w.Volume2DElement)
    prp2.put(w.CAUCHYMECHVOLINTMETH, w.VES_CMVIM_STD)
    prp2.put(w.STIFFMETHOD, w.STIFF_ANALYTIC)
    prp2.put(w.MATERIAL, 2)
    app2.addProperty(prp2)

    # Elements for surface traction

    prp4 = w.ElementProperties(w.NodStress2DElement)
    nod1 = w.NodInteraction(3)
    nod1.push(groups['DiskSide'])
    nod1.addProperty(prp4)
    iset.add(nod1)

    prp3 = w.ElementProperties(w.NodStress2DElement)
    nod2 = w.NodInteraction(4)
    nod2.push(groups['PeigneSide'])
    nod2.push(groups['Clamped'])
    nod2.addProperty(prp3)
    iset.add(nod2)

    parm['interaction_M'] = [nod1, nod2]
    parm['polytope'] = [nod1.getElementSet(), nod2.getElementSet()]

    # Contact properties

    prp5 = w.ElementProperties(w.Contact2DElement)
    prp5.put(w.AREAINCONTACT, w.AIC_ONCE)
    prp5.put(w.MATERIAL, 3)

    # Defines the contact entities

    ci = w.DdContactInteraction(5)
    ci.setTool(groups['PeigneSide'])
    ci.setSmoothNormals(False)
    ci.push(groups['DiskSide'])
    ci.setSinglePass()
    ci.addProperty(prp5)
    iset.add(ci)

    # Boundary conditions

    loadset = domain.getLoadingSet()
    loadset.define(groups['Clamped'], w.Field1D(w.TX, w.RE))
    loadset.define(groups['Clamped'], w.Field1D(w.TY, w.RE))

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

    # Nodal GMSH extractor

    ext = w.GmshNodalExtractor(metafor, 'metafor/output')
    ext.add(1, w.IFNodalValueExtractor(groups['Disk'], w.IF_EVMS))
    ext.add(2, w.IFNodalValueExtractor(groups['Peigne'], w.IF_EVMS))
    parm['extractor'] = ext

    # Build domain and folder

    domain.build()
    parm['FSInterface'] = groups['FSInterface']
    os.makedirs('metafor')
    return metafor