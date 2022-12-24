from ..toolbox import write_logs,compute_time
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

            self.dim = 2
            self.axe = [w.TX,w.TY]

        elif domain.getGeometry().is3D():
            
            self.dim = 3
            self.axe = [w.TX,w.TY,w.TZ]

        # Defines some internal variables

        self.Fnods = dict()
        self.neverRun = True
        self.reload = True

        # Defines some internal variables

        self.FSI = input['FSInterface']
        self.exporter = input['exporter']
        self.interaction = input['interaction']
        self.nbrNode = self.FSI.getNumberOfMeshPoints()
        self.prevLoad = np.zeros((self.nbrNode,self.dim))

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

        mean = (self.prevLoad+load)/2
        self.nextLoad = load.copy()

        for i in range(self.nbrNode):

            idx = self.FSI.getMeshPoint(i).getDBNo()
            if self.dim == 3: self.interaction.setNodValue(idx,*mean[i])
            else: self.interaction.setNodValue(idx,*mean[i],0)

# %% Gets Nodal Values

    def getPosition(self):

        posVec = np.zeros((self.nbrNode,self.dim))

        for i,axe in enumerate(self.axe):
            for j,position in enumerate(posVec):

                node = self.FSI.getMeshPoint(j)
                position[i] += node.getValue(w.Field1D(axe,w.AB))
                position[i] += node.getValue(w.Field1D(axe,w.RE))
        
        return posVec

    # Computes the nodal displacement vector

    def getDisplacement(self):

        dispVec = np.zeros((self.nbrNode,self.dim))

        for i,axe in enumerate(self.axe):
            for j,disp in enumerate(dispVec):

                node = self.FSI.getMeshPoint(j)
                disp[i] = node.getValue(w.Field1D(axe,w.RE))
        
        return dispVec

    # Computes the nodal velocity vector

    def getVelocity(self):

        velVec = np.zeros((self.nbrNode,self.dim))

        for i,axe in enumerate(self.axe):
            for j,velocity in enumerate(velVec):

                node = self.FSI.getMeshPoint(j)
                velocity[i] = node.getValue(w.Field1D(axe,w.GV))
        
        return velVec

    # Computes the nodal acceleration vector

    def getAcceleration(self):

        accVec = np.zeros((self.nbrNode,self.dim))

        for i,axe in enumerate(self.axe):
            for j,acc in enumerate(accVec):

                node = self.FSI.getMeshPoint(j)
                acc[j,i] = node.getValue(w.Field1D(axe,w.GA))
        
        return accVec

# %% Other Functions

    @compute_time
    def update(self):
        
        self.prevLoad = self.nextLoad.copy()
        self.metaFac.save(self.mfac)
        self.reload = False
        
    @compute_time
    def save(self):
        self.exporter.execute()

    def exit(self):
        return