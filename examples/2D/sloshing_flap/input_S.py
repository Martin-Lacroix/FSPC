import toolbox.gmsh as gmsh
import numpy as np
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

    # Dimension and DSS solver

    domain = metafor.getDomain()
    domain.getGeometry().setDimPlaneStrain(1)
    metafor.getSolverManager().setSolver(w.DSSolver())

    # define the rotation axis

    pointset = domain.getGeometry().getPointSet()
    pointset.define(1, 0, 0, -1)
    pointset.define(2, 0, 0, 1)
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__), 'geometry_S.msh')
    importer = gmsh.GmshImport(mshFile, domain)
    groups = importer.groups
    importer.execute()

    parm['FSInterface'] = groups['FSInterface']

    # Defines the solid domain

    iset = domain.getInteractionSet()
    app = w.FieldApplicator(1)
    app.push(groups['Solid'])
    iset.add(app)

    # Material parameters

    materset = domain.getMaterialSet()
    materset.define(1, w.ElastHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS, 6e6)
    materset(1).put(w.POISSON_RATIO, 0.45)
    materset(1).put(w.MASS_DENSITY, 1100)

    # Material parameters

    v = 0.4
    E = 6.14e6
    K = E/(3*(1-2*v))
    G = E/(2*(1+v))

    materset = domain.getMaterialSet()
    materset.define(1, w.NeoHookeanHyperPk2Material)
    materset(1).put(w.MASS_DENSITY, 1100)
    materset(1).put(w.HYPER_K0, K)
    materset(1).put(w.HYPER_G0, G)
    
    # Finite element properties

    prp1 = w.ElementProperties(w.Volume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH, w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD, w.STIFF_ANALYTIC)
    prp1.put(w.GRAVITY_Y, -9.81)
    prp1.put(w.MATERIAL, 1)
    app.addProperty(prp1)

    # Elements for surface traction

    prp2 = w.ElementProperties(w.NodStress2DElement)
    load = w.NodInteraction(2)
    load.push(groups['FSInterface'])
    load.push(groups['Clamped'])
    load.addProperty(prp2)
    iset.add(load)

    parm['interaction_M'] = load
    
    # Boundary conditions in degrees

    def theta(t):

        K = 4.9
        S = 2.144
        R = 2.278
        Q = 1.278

        den = Q*(1+np.exp(S-K*t))
        den += (R-Q)/(1+np.exp(t))
        den += (R-Q)*np.exp(S-K*t)/(1+np.exp(t))

        return 4*np.sin(2*np.pi*t/den)

    fct = w.PythonOneParameterFunction(theta)

    loadset = domain.getLoadingSet()
    loadset.defineRot(groups['Clamped'],
    w.Field3D(w.TXTYTZ, w.RE), pointset(1), pointset(2), False, 1, fct)

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
    ext.add(w.IFNodalValueExtractor(groups['Solid'], w.IF_P))
    ext.add(w.IFNodalValueExtractor(groups['Solid'], w.IF_EVMS))
    parm['exporter'] = ext

    # Build domain and folder

    domain.build()
    os.makedirs('metafor')
    return metafor