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

        # This function must be in Metafor !!!

        #if self.dim == 2: self.makeFaceList2D()
        #if self.dim == 3: self.makeFaceList3D()

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

        #if self.dim == 2: nLoad = self.integrate2D(load)
        #if self.dim == 3: nLoad = self.integrate3D(load)
        nLoad = load

        for i in range(self.nbrNode):

            node = self.FSI.getMeshPoint(i)
            nodeLoad = self.Fnods[node.getNo()]

            for j in range(len(nodeLoad)):

                nodeLoad[j].val2 = nLoad[i,j]
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

# %% # This Function Must be in Metafor !!!

    def makeFaceList2D(self):

        # List the curves with only 1 neighbor side

        facets = list()
        for i in range(self.nbrNode):

            node = self.FSI.getMeshPoint(i)
            curve = node.getCurves()

            for j in range(len(curve)):

                face = curve[j]
                if face.getNbOfUpSides() > 1: continue
                if face not in facets: facets.append(face)

        # List the number of FSI nodes for ach curve

        facetNodes = [[] for _ in range(len(facets))]
        for i in range(self.nbrNode):

            node = self.FSI.getMeshPoint(i)
            curve = node.getCurves()

            for j in range(len(curve)):

                face = curve[j]
                if face in facets:

                    idx = facets.index(face)
                    facetNodes[idx].append(i)

        # Keep the facets with 2 FSI nodes
        
        keep = list()
        for i in range(len(facetNodes)):
            if len(facetNodes[i]) == 2:
               keep.append(i)

        self.facetNodes = [facetNodes[q] for q in keep]
        self.facets = [facets[q] for q in keep]


    def makeFaceList3D(self):

        # List the sides with only 1 neighbor volume

        facets = list()
        for i in range(self.nbrNode):

            node = self.FSI.getMeshPoint(i)
            side = node.getSides()

            for j in range(len(side)):

                face = side[j]
                if face.getNbOfUpVolumes() > 1: continue
                if face not in facets: facets.append(face)

        # List the number of FSI nodes for each side

        facetNodes = [[] for _ in range(len(facets))]
        for i in range(self.nbrNode):

            node = self.FSI.getMeshPoint(i)
            sides = node.getSides()

            for j in range(len(sides)):

                face = sides[j]
                if face in facets:

                    idx = facets.index(face)
                    facetNodes[idx].append(i)

        # Keep only the facets with 4 FSI nodes
        
        keep = list()
        for i in range(len(facetNodes)):
            if len(facetNodes[i]) == 4:
               keep.append(i)

        self.facetNodes = [facetNodes[q] for q in keep]
        self.facets = [facets[q] for q in keep]

# %% This function must be in Metafor !!!

    def integrate2D(self,load):

        nLoad = np.zeros(load.shape)

        for i in range(len(self.facetNodes)):

            n1 = self.facetNodes[i][0]
            n2 = self.facetNodes[i][1]
            Sn = (load[n1]+load[n2])/2
            L = self.facets[i].length()*Sn

            nLoad[n1] += L/2
            nLoad[n2] += L/2
        
        return nLoad

    def integrate3D(self,load):

        nLoad = np.zeros(load.shape)

        for i in range(len(self.facetNodes)):

            n1 = self.facetNodes[i][0]
            n2 = self.facetNodes[i][1]
            n3 = self.facetNodes[i][2]
            n4 = self.facetNodes[i][3]
            
            Sn = (load[n1]+load[n2]+load[n3]+load[n4])/4
            L = self.facets[i].area()*Sn

            nLoad[n1] += L/4
            nLoad[n2] += L/4
            nLoad[n3] += L/4
            nLoad[n4] += L/4
        
        return nLoad