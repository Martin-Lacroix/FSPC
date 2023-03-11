from ..toolbox import write_logs,compute_time
from toolbox.fac import FacManager
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

        input = dict()
        self.metafor = module.getMetafor(input)
        self.tsm = self.metafor.getTimeStepManager()
        domain = self.metafor.getDomain()
        domain.build()

        # Sets the dimension of the mesh

        if domain.getGeometry().is2D():

            length = 3
            self.dim = 2
            self.axe = [w.TX,w.TY]

        elif domain.getGeometry().is3D():
            
            length = 6
            self.dim = 3
            self.axe = [w.TX,w.TY,w.TZ]

        # Defines some internal variables

        self.mecha = True
        self.reload = True
        self.thermo = True
        self.neverRun = True
        self.FSI = input['FSInterface']
        self.exporter = input['exporter']
        self.nbrNode = self.FSI.getNumberOfMeshPoints()
        self.metafor.getInitialConditionSet().update(0)

        # Mechanical and thermal interactions

        try:
            self.interacM = input['interacM']
            self.prevLoad = np.zeros((self.nbrNode,length))
        except: self.mecha = False

        try:
            self.interacT = input['interacT']
            self.prevHeat = np.zeros((self.nbrNode,self.dim))
        except: self.thermo = False

        # Manages time step restart functions

        self.mfac = w.MemoryFac()
        self.metaFac = w.MetaFac(self.metafor)
        self.metaFac.mode(False,False,True)
        self.metaFac.save(self.mfac)
        self.tsm.setVerbose(False)

# %% Calculates One Time Step
    
    @write_logs
    @compute_time
    def run(self,t1,t2):

        if(self.neverRun):

            self.tsm.setInitialTime(t1,t2-t1)
            self.tsm.setNextTime(t2,0,t2-t1)
            ok = self.metafor.getTimeIntegration().integration()
            self.neverRun = False

        else:

            if self.reload: self.tsm.removeLastStage()
            self.tsm.setNextTime(t2,0,t2-t1)
            ok = self.metafor.getTimeIntegration().restart(self.mfac)

        self.reload = True
        return ok

# %% Set Nodal Loads

    def applyLoading(self,load):

        vector = (self.prevLoad+load)/2
        self.nextLoad = np.copy(load)

        for i in range(self.nbrNode):

            node = self.FSI.getMeshPoint(i)
            self.interacM.setNodTensor(node,*vector[i])

    def applyHeatFlux(self,heat):

        vector = (self.prevHeat+heat)/2
        self.nextHeat = np.copy(heat)

        for i in range(self.nbrNode):

            node = self.FSI.getMeshPoint(i)
            self.interacT.setNodVector(node,*vector[i])

# %% Return Mechanical Nodal Values

    def getPosition(self):

        vector = np.zeros((self.nbrNode,self.dim))

        for i,axe in enumerate(self.axe):
            for j,data in enumerate(vector):

                node = self.FSI.getMeshPoint(j)
                data[i] += node.getValue(w.Field1D(axe,w.AB))
                data[i] += node.getValue(w.Field1D(axe,w.RE))

        return vector

    # Computes the nodal displacement vector

    def getDisplacement(self):

        vector = np.zeros((self.nbrNode,self.dim))

        for i,axe in enumerate(self.axe):
            for j,data in enumerate(vector):

                node = self.FSI.getMeshPoint(j)
                data[i] = node.getValue(w.Field1D(axe,w.RE))
        
        return vector

    # Computes the nodal velocity vector

    def getVelocity(self):

        vector = np.zeros((self.nbrNode,self.dim))

        for i,axe in enumerate(self.axe):
            for j,data in enumerate(vector):

                node = self.FSI.getMeshPoint(j)
                data[i] = node.getValue(w.Field1D(axe,w.GV))
        
        return vector

    # Computes the nodal acceleration vector

    def getAcceleration(self):

        vector = np.zeros((self.nbrNode,self.dim))

        for i,axe in enumerate(self.axe):
            for j,data in enumerate(vector):

                node = self.FSI.getMeshPoint(j)
                data[j,i] = node.getValue(w.Field1D(axe,w.GA))
        
        return vector

# %% Return Thermal Nodal Values

    def getTemperature(self):

        vector = np.zeros((self.nbrNode,1))
        
        for i in range(self.nbrNode):

            node = self.FSI.getMeshPoint(i)
            vector[i,0] += node.getValue(w.Field1D(w.TO,w.AB))
            vector[i,0] += node.getValue(w.Field1D(w.TO,w.RE))

        return vector

    # Computes the nodal temperature velocity

    def getTempVeloc(self):

        vector = np.zeros((self.nbrNode,1))

        for i in range(self.nbrNode):

            node = self.FSI.getMeshPoint(i)
            vector[i] = node.getValue(w.Field1D(w.TO,w.GV))
        
        return vector

# %% Other Functions

    @compute_time
    def update(self):
        
        if self.mecha: self.prevLoad = np.copy(self.nextLoad)
        if self.thermo: self.prevHeat = np.copy(self.nextHeat)
        self.metaFac.save(self.mfac)
        self.reload = False

    @write_logs
    @compute_time
    def save(self): self.exporter.execute()
    def exit(self): return