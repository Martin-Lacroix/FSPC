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
    loadingset = domain.getLoadingSet()
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

    # Defines the ball domain

    app1 = w.FieldApplicator(1)
    app1.push(groups['Copper'])
    interactionset.add(app1)

    app2 = w.FieldApplicator(2)
    app2.push(groups['Iron'])
    interactionset.add(app2)

    # Copper material parameters

    materset.define(1,w.TmElastHypoMaterial)
    materset(1).put(w.ELASTIC_MODULUS,1.1e11)
    materset(1).put(w.THERM_EXPANSION,17.6e-6)
    materset(1).put(w.HEAT_CAPACITY,385)
    materset(1).put(w.MASS_DENSITY,8960)
    materset(1).put(w.POISSON_RATIO,0.343)
    materset(1).put(w.CONDUCTIVITY,413)
    materset(1).put(w.DISSIP_TE,0)
    materset(1).put(w.DISSIP_TQ,0)

    # Iron material parameters

    materset.define(2,w.TmElastHypoMaterial)
    materset(2).put(w.ELASTIC_MODULUS,2e11)
    materset(2).put(w.THERM_EXPANSION,12.2e-6)
    materset(2).put(w.HEAT_CAPACITY,450)
    materset(2).put(w.MASS_DENSITY,7874)
    materset(2).put(w.POISSON_RATIO,0.291)
    materset(2).put(w.CONDUCTIVITY,94)
    materset(2).put(w.DISSIP_TE,0)
    materset(2).put(w.DISSIP_TQ,0)

    # Finite element properties

    prp1 = w.ElementProperties(w.TmVolume2DElement)
    prp1.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_SRIPR)
    prp1.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp1.put(w.MATERIAL,1)
    app1.addProperty(prp1)

    prp2 = w.ElementProperties(w.TmVolume2DElement)
    prp2.put(w.CAUCHYMECHVOLINTMETH,w.VES_CMVIM_SRIPR)
    prp2.put(w.STIFFMETHOD,w.STIFF_ANALYTIC)
    prp2.put(w.MATERIAL,2)
    app2.addProperty(prp2)

    # Elements for surface heat flux

    prp3 = w.ElementProperties(w.NodHeatFlux2DElement)
    heat = w.NodInteraction(3)
    heat.push(groups['FSInterface'])
    heat.addProperty(prp3)
    interactionset.add(heat)

    # Elements for surface traction

    prp4 = w.ElementProperties(w.NodStress2DElement)
    load = w.NodInteraction(4)
    load.push(groups['FSInterface'])
    load.addProperty(prp4)
    interactionset.add(load)

    # Boundary conditions

    loadingset.define(groups['Clamped'],w.Field1D(w.TX,w.RE))
    loadingset.define(groups['Clamped'],w.Field1D(w.TY,w.RE))
    initcondset.define(groups['Iron'],w.Field1D(w.TO,w.AB),293.15)
    initcondset.define(groups['Copper'],w.Field1D(w.TO,w.AB),293.15)

    # Mechanical and thermal time integration

    ti_M = w.AlphaGeneralizedTimeIntegration(metafor)
    ti_T = w.TrapezoidalThermalTimeIntegration(metafor)

    ti = w.StaggeredTmTimeIntegration(metafor)
    ti.setMechanicalTimeIntegration(ti_M)
    ti.setThermalTimeIntegration(ti_T) 
    metafor.setTimeIntegration(ti)

    # Mechanical and thermal iterations

    mim.setMaxNbOfIterations(25)
    mim.setResidualTolerance(1e-4)

    tim.setMaxNbOfIterations(25)
    tim.setResidualTolerance(1e-4)

    # Time step iterations
    
    tscm = w.NbOfStaggeredTmNRIterationsTimeStepComputationMethod(metafor)
    tsm.setTimeStepComputationMethod(tscm)
    tscm.setTimeStepDivisionFactor(2)
    tscm.setNbOptiIte(25)

    # Parameters for FSPC

    input['interacT'] = heat
    input['interacM'] = load
    input['FSInterface'] = groups['FSInterface']
    input['exporter'] = gmsh.GmshExport('metafor/output.msh',metafor)
    input['exporter'].addInternalField([w.IF_EVMS,w.IF_P])
    input['exporter'].addDataBaseField([w.TO])
    input['exporter'].binary = True
    return metafor