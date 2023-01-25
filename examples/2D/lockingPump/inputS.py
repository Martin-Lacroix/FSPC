import toolbox.meshio as meshio
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
    loadingset = domain.getLoadingSet()
    solvermanager = metafor.getSolverManager()
    interactionset = domain.getInteractionSet()
    mim = metafor.getMechanicalIterationManager()

    # Dimension and DSS solver

    domain.getGeometry().setDimPlaneStrain(1)
    solvermanager.setSolver(w.DSSolver())
    
    # Imports the mesh

    mshFile = os.path.join(os.path.dirname(__file__),'geometryS.msh')
    importer = meshio.MeshioImport(mshFile,metafor)
    groups = importer.groups
    importer.execute()
    
    # Defines the solid domain

    app1 = w.FieldApplicator(1)
    app1.push(groups['Top'])
    app1.push(groups['Bot'])
    interactionset.add(app1)
    
    # Solid material parameters

    v = 0.3
    E = 2000
    G = E/(2*(1+v))
    K = E/(3*(1-2*v))

    materset.define(1,w.NeoHookeanHyperPk2Material)
    materset(1).put(w.MASS_DENSITY,1e-3)
    materset(1).put(w.HYPER_K0,K)
    materset(1).put(w.HYPER_G0,G)

    # Contact parameters

    materset.define(2,w.FrictionlessContactMaterial)
    materset(2).put(w.PEN_NORMALE,1e4)
    materset(2).put(w.PROF_CONT,0.01)
    
    # Volume solid properties

    prp1 = w.ElementProperties(w.TriangleVolume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_STD)
    prp1.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp1.put(w.MATERIAL,1)
    app1.addProperty(prp1)

    # Elements for surface traction

    prp2 = w.ElementProperties(w.NodTraction2DElement)
    load = w.NodInteraction(2)
    load.push(groups['FSInterface'])
    load.addProperty(prp2)
    interactionset.add(load)

    # Contact properties

    prp3 = w.ElementProperties(w.Contact2DElement)
    prp3.put(w.AREAINCONTACT,w.AIC_ONCE)
    prp3.put(w.MATERIAL,2)

    # Defines the contact entities

    ci = w.DdContactInteraction(3)
    ci.setTool(groups['Master'])
    ci.setSmoothNormals(False)
    ci.push(groups['Slave'])
    ci.setSinglePass()
    ci.addProperty(prp3)
    interactionset.add(ci)

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

    input['interacM'] = load
    input['FSInterface'] = groups['FSInterface']
    input['exporter'] = meshio.MeshioExport('metafor/solid.msh',metafor)
    input['exporter'].addInternalField([w.IF_EVMS,w.IF_P])
    input['exporter'].format = 'gmsh'
    return metafor