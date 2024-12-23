import toolbox.gmsh as gmsh
import wrap as w
import os

metafor = None
def getMetafor(parm):
    '''
    Initialize and return the metafor object
    '''

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

    # Make the revolution tool

    L1 = 0.3
    L2 = 0.5
    L3 = 0.8
    R1 = 0.3

    B = 0.15
    S = 0.04

    geometry = domain.getGeometry()
    pointset = geometry.getPointSet()

    # Points list

    pointset.define(1, L1+L2+L3+S, S-R1, 0)
    pointset.define(2, L1+L2+S, S-R1, 0)
    pointset.define(3, L1+L2+S, -B, 0)
    pointset.define(4, L1+L2+S/2, S/2-B, 0)
    pointset.define(5, L1+L2, -B, 0)
    pointset.define(6, L1+L2, S-R1, 0)
    pointset.define(7, L1, S-R1, 0)

    pointset.define(8, L1, R1-S, 0)
    pointset.define(9, L1+L2, R1-S, 0)
    pointset.define(10, L1+L2, B, 0)
    pointset.define(11, L1+L2+S/2, B-S/2, 0)
    pointset.define(12, L1+L2+S, B, 0)
    pointset.define(13, L1+L2+S, R1-S, 0)
    pointset.define(14, L1+L2+L3+S, R1-S, 0)

    # Curve list

    curveset = geometry.getCurveSet()

    curveset.add(w.Line(1, pointset(1), pointset(2)))
    curveset.add(w.Line(2, pointset(2), pointset(3)))
    curveset.add(w.Arc(3, pointset(3), pointset(4), pointset(5)))
    curveset.add(w.Line(4, pointset(5), pointset(6)))
    curveset.add(w.Line(5, pointset(6), pointset(7)))

    curveset.add(w.Line(6, pointset(8), pointset(9)))
    curveset.add(w.Line(7, pointset(9), pointset(10)))
    curveset.add(w.Arc(8, pointset(10), pointset(11), pointset(12)))
    curveset.add(w.Line(9, pointset(12), pointset(13)))
    curveset.add(w.Line(10, pointset(13), pointset(14)))

    # Generate the contact tool

    wireset = geometry.getWireSet()
    wireset.add(w.Wire(1, [curveset(i) for i in range(1, 11)]))
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__), 'geometry_S.msh')
    importer = gmsh.GmshImport(mshFile, domain)
    groups = importer.groups
    importer.execute()

    parm['FSI'] = groups['FSI']
    
    # Defines the solid domain

    iset = domain.getInteractionSet()
    app = w.FieldApplicator(1)
    app.push(groups['Solid'])
    iset.add(app)
    
    # Solid material parameters

    materset = domain.getMaterialSet()
    materset.define(1, w.EvpIsoHHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS, 1e7)
    materset(1).put(w.MASS_DENSITY, 1e3)
    materset(1).put(w.POISSON_RATIO, 0)
    materset(1).put(w.YIELD_NUM, 1)

    lawset = domain.getMaterialLawSet()
    lawset.define(1, w.SwiftIsotropicHardening)
    lawset(1).put(w.IH_SIGEL, 1e5)
    lawset(1).put(w.IH_B, 375)
    lawset(1).put(w.IH_N, 0.2)

    # Contact parameters

    penalty = 1e7
    friction = 0.15

    materset.define(2, w.CoulombContactMaterial)
    materset(2).put(w.PEN_TANGENT, friction*penalty)
    materset(2).put(w.COEF_FROT_DYN, friction)
    materset(2).put(w.COEF_FROT_STA, friction)
    materset(2).put(w.PEN_NORMALE, penalty)
    materset(2).put(w.PROF_CONT, 0.01)

    # Volume solid properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH, w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD, w.STIFF_ANALYTIC)
    prp1.put(w.GRAVITY_Y, -9.81)
    prp1.put(w.MATERIAL, 1)
    app.addProperty(prp1)

    # Elements for surface traction

    prp2 = w.ElementProperties(w.NodStress2DElement)
    load = w.NodInteraction(2)
    load.push(groups['FSI'])
    load.addProperty(prp2)
    iset.add(load)

    parm['interaction_M'] = load

    # Contact properties

    prp3 = w.ElementProperties(w.Contact2DElement)
    prp3.put(w.AREAINCONTACT, w.AIC_ONCE)
    prp3.put(w.MATERIAL, 2)

    # Contact for Tool and Solid

    ci = w.RdContactInteraction(3)
    ci.setTool(wireset(1))
    ci.setSmoothNormals(False)
    ci.push(groups['FSI'])
    ci.addProperty(prp3)
    iset.add(ci)

    # Boundary conditions

    loadset = domain.getLoadingSet()
    loadset.define(wireset(1), w.Field1D(w.TX, w.RE))
    loadset.define(wireset(1), w.Field1D(w.TY, w.RE))

    # Mechanical time integration

    ti = w.AlphaGeneralizedTimeIntegration(metafor)
    metafor.setTimeIntegration(ti)

    # Mechanical iterations

    mim = metafor.getMechanicalIterationManager()
    mim.setResidualTolerance(1e-6)
    mim.setMaxNbOfIterations(25)

    # Time step iterations
    
    tsm = metafor.getTimeStepManager()
    tscm = w.NbOfMechNRIterationsTimeStepComputationMethod(metafor)
    tsm.setTimeStepComputationMethod(tscm)
    tscm.setTimeStepDivisionFactor(2)
    tscm.setNbOptiIte(25)

    # Nodal Gmsh exporter

    ext = w.GmshExporter(metafor, 'metafor/output')
    ext.add(w.IFNodalValueExtractor(groups['Solid'], w.IF_EVMS))
    ext.add(w.IFNodalValueExtractor(groups['Solid'], w.IF_EPL))
    parm['exporter'] = ext

    # Build domain and folder

    domain.build()
    os.makedirs('metafor')
    return metafor