import toolbox.gmsh as gmsh
import wrap as w
import os

# %% Main Function

metafor = None
def getMetafor(param):

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
    tim = metafor.getThermalIterationManager()
    solvermanager = metafor.getSolverManager()
    interactionset = domain.getInteractionSet()
    mim = metafor.getMechanicalIterationManager()
    initcondset = metafor.getInitialConditionSet()

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
    app.push(groups['Solid_1'])
    app.push(groups['Solid_2'])
    app.push(groups['Solid_3'])
    interactionset.add(app)

    # Solid material parameters

    materset.define(1,w.TmElastHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS,1e7)
    materset(1).put(w.THERM_EXPANSION,0)
    materset(1).put(w.HEAT_CAPACITY,100)
    materset(1).put(w.MASS_DENSITY,950)
    materset(1).put(w.POISSON_RATIO,0)
    materset(1).put(w.CONDUCTIVITY,5)
    materset(1).put(w.DISSIP_TE,0)
    materset(1).put(w.DISSIP_TQ,0)

    # Finite element properties

    prp1 = w.ElementProperties(w.TmVolume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_SRIPR)
    prp1.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp1.put(w.GRAVITY_Y,-9.81)
    prp1.put(w.MATERIAL,1)
    app.addProperty(prp1)

    # Elements for surface heat flux

    prp2 = w.ElementProperties(w.NodHeatFlux2DElement)
    heat = w.NodInteraction(2)
    heat.push(groups['FSInterface'])
    heat.addProperty(prp2)
    interactionset.add(heat)

    # Elements for surface traction

    prp3 = w.ElementProperties(w.NodStress2DElement)
    load = w.NodInteraction(3)
    load.push(groups['FSInterface'])
    load.addProperty(prp3)
    interactionset.add(load)

    # Initial and boundary conditions

    initcondset.define(groups['Solid_1'],w.Field1D(w.TO,w.AB),180)
    initcondset.define(groups['Solid_2'],w.Field1D(w.TO,w.AB),200)
    initcondset.define(groups['Solid_3'],w.Field1D(w.TO,w.AB),220)

    # Mechanical and thermal time integration

    ti_M = w.AlphaGeneralizedTimeIntegration(metafor)
    ti_T = w.TrapezoidalThermalTimeIntegration(metafor)

    ti = w.StaggeredTmTimeIntegration(metafor)
    ti.setMechanicalTimeIntegration(ti_M)
    ti.setThermalTimeIntegration(ti_T) 
    metafor.setTimeIntegration(ti)

    # Mechanical and thermal iterations

    mim.setMaxNbOfIterations(25)
    mim.setResidualTolerance(1e-6)

    tim.setMaxNbOfIterations(25)
    tim.setResidualTolerance(1e-6)

    # Time step iterations
    
    tscm = w.NbOfStaggeredTmNRIterationsTimeStepComputationMethod(metafor)
    tsm.setTimeStepComputationMethod(tscm)
    tscm.setTimeStepDivisionFactor(2)
    tscm.setNbOptiIte(25)

    # Parameters for FSPC

    param['interacT'] = heat
    param['interacM'] = load
    param['FSInterface'] = groups['FSInterface']
    param['exporter'] = gmsh.GmshExport('metafor/output.msh',metafor)
    param['exporter'].addDataBaseField([w.TO])
    param['exporter'].binary = True
    return metafor