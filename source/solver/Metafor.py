import numpy as np
import wrap as w
import importlib

# %% Nodal Load class

class NLoad(object):
    def __init__(self,val1,t1,val2,t2):

        self.t1 = t1
        self.t2 = t2
        self.val1 = val1
        self.val2 = val2

    def __call__(self,time):

        return self.val1+(time-self.t1)/(self.t2-self.t1)*(self.val2-self.val1)

    def nextstep(self):

        self.t1 = self.t2
        self.val1 = self.val2

# %% Initializes the Solid Wraper

class Metafor(object):
    def __init__(self,param):

        input = dict()
        module = importlib.import_module(param['inputS'])
        self.metafor = module.getMetafor(input)
        domain = self.metafor.getDomain()

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
        loadingset = domain.getLoadingSet()
        self.tsm = self.metafor.getTimeStepManager()
        self.nbrNode = self.FSI.getNumberOfMeshPoints()

        # Creates the nodal load container

        for i in range(self.nbrNode):
            
            load = list()
            node = self.FSI.getMeshPoint(i)
            self.Fnods[node.getNo()] = load

            for T in self.axe:

                load.append(NLoad(0,0,0,0))
                fct = w.PythonOneParameterFunction(load[-1])
                loadingset.define(node,w.Field1D(T,w.GF1),1,fct)

        # Initialization of domain and output

        self.metafor.getDomain().build()
        self.save()

        # Manages time step restart functions

        self.mfac = w.MemoryFac()
        self.metaFac = w.MetaFac(self.metafor)
        self.metaFac.mode(False,False,True)
        self.metaFac.save(self.mfac)
        self.tsm.setVerbose(False)

# %% Calculates One Time Step
        
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

    def applyLoading(self,load,time):

        for i in range(self.nbrNode):

            node = self.FSI.getMeshPoint(i)
            nodeLoad = self.Fnods[node.getNo()]

            for j in range(len(nodeLoad)):

                nodeLoad[j].val2 = load[i,j]
                nodeLoad[j].t2 = time
        
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

    def update(self):
        
        for nodeLoad in self.Fnods.values():
            for i in range(self.dim): nodeLoad[i].nextstep()
        
        self.metaFac.save(self.mfac)
        self.reload = False

    def save(self):
        self.exporter.execute()

    def exit(self):
        return