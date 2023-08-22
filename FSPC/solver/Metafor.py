from ..general import Toolbox as tb
import importlib.util as util
import numpy as np
import wrap as w
import sys

# %% Initializes the Solid Wraper

class Metafor(object):
    def __init__(self,path):
        
        # Convert Metafor into a module

        spec = util.spec_from_file_location('module.name',path)
        module = util.module_from_spec(spec)
        sys.modules['module.name'] = module
        spec.loader.exec_module(module)

        # Actually initialize Metafor from file

        parm = dict()
        self.metafor = module.getMetafor(parm)
        self.tsm = self.metafor.getTimeStepManager()
        geometry = self.metafor.getDomain().getGeometry()
        self.metafor.getDomain().build()

        # Sets the dimension of the mesh

        if geometry.is2D():

            self.dim = 2
            self.axe = [w.TX,w.TY]
            if geometry.isAxisymmetric(): size = 4
            else: size = 3

        elif geometry.is3D():
            
            size = 6
            self.dim = 3
            self.axe = [w.TX,w.TY,w.TZ]

        # Defines some internal variables

        self.reload = True
        self.neverRun = True
        self.FSI = parm['FSInterface']
        self.exporter = parm['exporter']
        self.nbrNod = self.FSI.getNumberOfMeshPoints()
        self.metafor.getInitialConditionSet().update(0)

        # Mechanical and thermal interactions

        if 'interacM' in parm:

            self.interacM = parm['interacM']
            self.prevLoad = np.zeros((self.nbrNod,size))

        if 'interacT' in parm:
            
            self.interacT = parm['interacT']
            self.prevHeat = np.zeros((self.nbrNod,self.dim))

        # Manages time step restart functions

        self.mfac = w.MemoryFac()
        self.metaFac = w.MetaFac(self.metafor)
        self.metaFac.mode(False,False,True)
        self.metaFac.save(self.mfac)
        self.tsm.setVerbose(False)

# %% Calculates One Time Step
    
    @tb.write_logs
    @tb.compute_time
    def run(self):

        if(self.neverRun):

            self.tsm.setInitialTime(tb.step.time,tb.step.dt)
            self.tsm.setNextTime(tb.step.nexTime(),0,tb.step.dt)
            ok = self.metafor.getTimeIntegration().integration()
            self.neverRun = False

        else:

            if self.reload: self.tsm.removeLastStage()
            self.tsm.setNextTime(tb.step.nexTime(),0,tb.step.dt)
            ok = self.metafor.getTimeIntegration().restart(self.mfac)

        self.reload = True
        return ok

# %% Set Nodal Loads

    def applyLoading(self,load):

        vector = (self.prevLoad+load)/2
        self.nextLoad = np.copy(load)

        for i in range(self.nbrNod):

            node = self.FSI.getMeshPoint(i)
            self.interacM.setNodTensor(node,*vector[i])

    def applyHeatFlux(self,heat):

        vector = (self.prevHeat+heat)/2
        self.nextHeat = np.copy(heat)

        for i in range(self.nbrNod):

            node = self.FSI.getMeshPoint(i)
            self.interacT.setNodVector(node,*vector[i])

# %% Return Mechanical Nodal Values

    def getPosition(self):

        vector = np.zeros((self.nbrNod,self.dim))

        for i,axe in enumerate(self.axe):
            for j,data in enumerate(vector):

                node = self.FSI.getMeshPoint(j)
                data[i] += node.getValue(w.Field1D(axe,w.AB))
                data[i] += node.getValue(w.Field1D(axe,w.RE))

        return vector

    # Computes the nodal velocity vector

    def getVelocity(self):

        vector = np.zeros((self.nbrNod,self.dim))

        for i,axe in enumerate(self.axe):
            for j,data in enumerate(vector):

                node = self.FSI.getMeshPoint(j)
                data[i] = node.getValue(w.Field1D(axe,w.GV))
        
        return vector

# %% Return Thermal Nodal Values

    def getTemperature(self):

        vector = np.zeros((self.nbrNod,1))
        
        for i in range(self.nbrNod):

            node = self.FSI.getMeshPoint(i)
            vector[i,0] += node.getValue(w.Field1D(w.TO,w.AB))
            vector[i,0] += node.getValue(w.Field1D(w.TO,w.RE))

        return vector

    # Computes the nodal temperature velocity

    def getTempVeloc(self):

        vector = np.zeros((self.nbrNod,1))

        for i in range(self.nbrNod):

            node = self.FSI.getMeshPoint(i)
            vector[i] = node.getValue(w.Field1D(w.TO,w.GV))
        
        return vector

# %% Other Functions

    @tb.compute_time
    def update(self):
        
        if tb.convMech: self.prevLoad = np.copy(self.nextLoad)
        if tb.convTher: self.prevHeat = np.copy(self.nextHeat)
        self.metaFac.save(self.mfac)
        self.reload = False

    @tb.write_logs
    @tb.compute_time
    def save(self): self.exporter.execute()
    def exit(self): return

# %% FSI Facets Relative to Each Node

    @tb.compute_time
    def getFacet(self):

        nbrList = np.zeros(self.nbrNod,dtype=int)
        try: elemSet = self.interacM.getElementSet()
        except: elemSet = self.interacT.getElementSet()

        # Store the node indices from Metafor

        faceList = list()
        for i in range(self.nbrNod):
            nbrList[i] = self.FSI.getMeshPoint(i).getNo()

        # Facet nodes and store their FSI indices

        for i in range(elemSet.size()):
            
            faceList.append(list())
            element = elemSet.getElement(i).getMyMesh()

            for j in range(element.getNbOfDownPoints()):

                ref = element.getDownPoint(j).getNo()
                index = np.argwhere(nbrList == ref).item()
                faceList[-1].append(index)

        return np.array(faceList)