from ..general import Toolbox as tb
import importlib.util as util
import numpy as np
import wrap as w
import sys

# |-----------------------------------|
# |   Initializes the Solid Wraper    |
# |-----------------------------------|

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
        self.metafor.getInitialConditionSet().update(0)
        self.dim = geometry.getDimension().getNdim()
        self.metafor.getDomain().build()

        # Sets the dimension of the mesh

        if geometry.is2D():

            size = 3
            self.axis = [w.TX,w.TY]
            tensor = 'setNodTensor2D'

        if geometry.isAxisymmetric():

            size = 4
            self.axis = [w.TX,w.TY]
            tensor = 'setNodTensorAxi'

        if geometry.is3D():

            size = 6
            self.axis = [w.TX,w.TY,w.TZ]
            tensor = 'setNodTensor3D'

        # Defines some internal variables

        self.reload = True
        self.neverRun = True
        self.FSI = parm['FSInterface']
        self.exporter = parm['exporter']
        self.nbrNod = self.FSI.getNumberOfMeshPoints()
        self.prevPos = self.getPosition()

        # Mechanical and thermal interactions

        if 'interacM' in parm:

            self.interac = parm['interacM']
            self.prevLoad = np.zeros((self.nbrNod,size))
            self.setNodLoad = getattr(self.interac,tensor)

        if 'interacT' in parm:
            
            self.interac = parm['interacT']
            self.prevHeat = np.zeros((self.nbrNod,self.dim))

        # Manages time step and restart functions

        self.mfac = w.MemoryFac()
        self.metaFac = w.MetaFac(self.metafor)
        self.metaFac.mode(False,False,True)
        self.metaFac.save(self.mfac)
        self.tsm.setVerbose(False)

# |-------------------------------|
# |   Calculates One Time Step    |
# |-------------------------------|
    
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

# |----------------------------------|
# |   Neumann Boundary Conditions    |
# |----------------------------------|

    def applyLoading(self,load):

        self.nextLoad = np.copy(load)
        result = (self.prevLoad+load)/2

        for i in range(self.nbrNod):
            self.setNodLoad(self.FSI.getMeshPoint(i),*result[i])

    # Apply Thermal boundary conditions

    def applyHeatFlux(self,heat):

        self.nextHeat = np.copy(heat)
        result = (self.prevHeat+heat)/2

        for i in range(self.nbrNod):

            node = self.FSI.getMeshPoint(i)
            self.interac.setNodVector(node,*result[i])

# |-------------------------------------|
# |   Return Mechanical Nodal Values    |
# |-------------------------------------|

    def getDisplacement(self):
        return self.getPosition()-self.prevPos

    # Computes the nodal position vector

    def getPosition(self):

        result = np.zeros((self.nbrNod,self.dim))

        for i,axe in enumerate(self.axis):
            for j,data in enumerate(result):

                node = self.FSI.getMeshPoint(j)
                data[i] += node.getValue(w.Field1D(axe,w.AB))
                data[i] += node.getValue(w.Field1D(axe,w.RE))

        return result

    # Computes the nodal velocity result

    def getVelocity(self):

        result = np.zeros((self.nbrNod,self.dim))

        for i,axe in enumerate(self.axis):
            for j,data in enumerate(result):

                node = self.FSI.getMeshPoint(j)
                data[i] = node.getValue(w.Field1D(axe,w.GV))
        
        return result

# |----------------------------------|
# |   Return Thermal Nodal Values    |
# |----------------------------------|

    def getTemperature(self):

        result = np.zeros((self.nbrNod,1))
        
        for i in range(self.nbrNod):

            node = self.FSI.getMeshPoint(i)
            result[i] += node.getValue(w.Field1D(w.TO,w.AB))
            result[i] += node.getValue(w.Field1D(w.TO,w.RE))

        return result

    # Computes the nodal temperature velocity

    def getTempVeloc(self):

        result = np.zeros((self.nbrNod,1))

        for i in range(self.nbrNod):

            node = self.FSI.getMeshPoint(i)
            result[i] = node.getValue(w.Field1D(w.TO,w.GV))
        
        return result

# |------------------------------|
# |   Other Wrapper Functions    |
# |------------------------------|

    @tb.compute_time
    def update(self):
        
        if tb.convMech: self.prevLoad = np.copy(self.nextLoad)
        if tb.convTher: self.prevHeat = np.copy(self.nextHeat)
        self.prevPos = self.getPosition()
        self.metaFac.save(self.mfac)
        self.reload = False

    @tb.write_logs
    @tb.compute_time
    def save(self): self.exporter.execute()
    def exit(self): return

# |---------------------------------------|
# |   FSI Facets Relative to Each Node    |
# |---------------------------------------|

    @tb.compute_time
    def getFacet(self):

        elemSet = self.interac.getElementSet()
        nbrList = np.zeros(self.nbrNod,dtype=int)

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