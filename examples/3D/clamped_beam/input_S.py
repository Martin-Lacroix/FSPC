import toolbox.gmsh as gmsh
from wrap import mtCompositesw as cw
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
    domain.getGeometry().setDim3D()
    metafor.getSolverManager().setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__), 'geometry_S.msh')
    importer = gmsh.GmshImport(mshFile, domain)
    groups = importer.groups
    importer.execute()

    parm['FSInterface'] = groups['FSInterface']

    # Defines the ball domain

    iset = domain.getInteractionSet()
    app = w.FieldApplicator(1)
    app.push(groups['Solid'])
    iset.add(app)

    # Solid material parameters

    materset = domain.getMaterialSet()
    materset.define(1, cw.ElastOrthoHypoMaterial)
    materset(1).put(w.MASS_DENSITY, 2e3)

    materset(1).put(cw.YOUNG_MODULUS_1, 70e9)
    materset(1).put(cw.YOUNG_MODULUS_2, 39e9)
    materset(1).put(cw.YOUNG_MODULUS_3, 39e9)

    materset(1).put(cw.SHEAR_MODULUS_12, 20e9)
    materset(1).put(cw.SHEAR_MODULUS_13, 20e9)
    materset(1).put(cw.SHEAR_MODULUS_23, 15e9)

    materset(1).put(cw.POISSON_RATIO_12, 0.26)
    materset(1).put(cw.POISSON_RATIO_13, 0.26)
    materset(1).put(cw.POISSON_RATIO_23, 0.3)

    materset(1).put(w.ORTHO_AX1_X, 1)
    materset(1).put(w.ORTHO_AX1_Y, 0)
    materset(1).put(w.ORTHO_AX1_Z, 0)
    materset(1).put(w.ORTHO_AX2_X, 0)
    materset(1).put(w.ORTHO_AX2_Y, 1)
    materset(1).put(w.ORTHO_AX2_Z, 0)

    # Finite element properties

    prp1 = w.ElementProperties(w.Volume3DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH, w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD, w.STIFF_ANALYTIC)
    prp1.put(w.GRAVITY_Z, -9.81)
    prp1.put(w.MATERIAL, 1)
    app.addProperty(prp1)

    # Elements for surface traction

    prp2 = w.ElementProperties(w.NodStress3DElement)
    load = w.NodInteraction(2)
    load.push(groups['FSInterface'])
    load.addProperty(prp2)
    iset.add(load)

    parm['interaction_M'] = load

    # Boundary conditions
    
    loadset = domain.getLoadingSet()
    loadset.define(groups['Clamped'], w.Field1D(w.TX, w.RE))
    loadset.define(groups['Clamped'], w.Field1D(w.TY, w.RE))
    loadset.define(groups['Clamped'], w.Field1D(w.TZ, w.RE))

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

    # Nodal GMSH exporter

    ext = w.GmshExporter(metafor, 'metafor/output')
    ext.add(w.IFNodalValueExtractor(groups['Solid'], w.IF_SIG_XX))
    ext.add(w.DbNodalValueExtractor(groups['Solid'], w.Field1D(w.TZ, w.GF1)))
    parm['exporter'] = ext

    # Build domain and folder

    domain.build()
    os.makedirs('metafor')
    return metafor
