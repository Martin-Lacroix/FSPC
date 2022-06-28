import numpy as np
import wrap as w
import importlib
import fwkw

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
        self.redirect = fwkw.StdOutErr2Py()
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

        pos = np.zeros((self.nbrNode,self.dim))

        for i in range(self.dim):
            for j in range(self.nbrNode):

                node = self.FSI.getMeshPoint(j)
                pos[j,i] += node.getValue(w.Field1D(self.axe[i],w.AB))
                pos[j,i] += node.getValue(w.Field1D(self.axe[i],w.RE))
        
        return pos

    # Computes the nodal displacement vector

    def getDisplacement(self):

        disp = np.zeros((self.nbrNode,self.dim))

        for i in range(self.dim):
            for j in range(self.nbrNode):

                node = self.FSI.getMeshPoint(j)
                disp[j,i] = node.getValue(w.Field1D(self.axe[i],w.RE))
        
        return disp

    # Computes the nodal velocity vector

    def getVelocity(self):

        vel = np.zeros((self.nbrNode,self.dim))

        for i in range(self.dim):
            for j in range(self.nbrNode):

                node = self.FSI.getMeshPoint(j)
                vel[j,i] = node.getValue(w.Field1D(self.axe[i],w.GV))
        
        return vel

    # Computes the nodal acceleration vector

    def getAcceleration(self):

        acc = np.zeros((self.nbrNode,self.dim))

        for i in range(self.dim):
            for j in range(self.nbrNode):

                node = self.FSI.getMeshPoint(j)
                acc[j,i] = node.getValue(w.Field1D(self.axe[i],w.GA))
        
        return acc

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