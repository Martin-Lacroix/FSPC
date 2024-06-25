from ..general import toolbox as tb
import importlib.util as util
import numpy as np
import wrap as w
import sys

# Solid solver wrapper class for Metafor

class Solver(object):
    def __init__(self, path: str):
        '''
        Initialize the solid solver wrapper class
        '''

        parm = dict()
        spec = util.spec_from_file_location('module.name', path)
        module = util.module_from_spec(spec)
        sys.modules['module.name'] = module
        spec.loader.exec_module(module)

        # Actually initialize Metafor from a file

        self.metafor = module.getMetafor(parm)
        self.geometry = self.metafor.getDomain().getGeometry()
        self.dim = self.geometry.getDimension().getNdim()
        self.tsm = self.metafor.getTimeStepManager()

        # Sets the dimension of the interaction

        if self.dim == 2: self.axis = (w.TX, w.TY)
        if self.dim == 3: self.axis = (w.TX, w.TY, w.TZ)

        # Defines some internal variables

        self.FSI = parm['FSInterface']
        self.exporter = parm['exporter']

        # Mechanical and thermal interactions

        if 'polytope' in parm:
            self.polytope = np.atleast_1d(parm['polytope'])

        if 'interaction_M' in parm:
            self.interaction_M = np.atleast_1d(parm['interaction_M'])

        if 'interaction_T' in parm:
            self.interaction_T = np.atleast_1d(parm['interaction_T'])

        # Create the memory fac used to restart

        self.fac = w.MemoryFac()
        self.meta_fac = w.MetaFac(self.metafor)
        self.meta_fac.mode(False, False, True)
        self.meta_fac.save(self.fac)

        # Initialize the integration and restart

        self.max_division = 200
        self.tsm.setInitialTime(0, np.inf)
        self.metafor.getInitialConditionSet().update(0)

    @tb.write_logs
    @tb.compute_time
    def run(self):
        '''
        Run the solid solver within the current time step
        '''

        self.tsm.setNextTime(tb.Step.next_time(), 0, tb.Step.dt)
        self.tsm.setMinimumTimeStep(tb.Step.dt/self.max_division)
        return self.metafor.getTimeIntegration().integration()

    def apply_loading(self, load: np.ndarray):
        '''
        Apply the loading from the fluid to the solid interface
        '''

        for interaction in self.interaction_M:
            for i, data in enumerate(load):

                node = self.FSI.getMeshPoint(i)

                if self.geometry.isAxisymmetric():
                    interaction.setNodTensorAxi(node, *data)

                elif self.geometry.is2D():
                    interaction.setNodTensor2D(node, *data)

                elif self.geometry.is3D():
                    interaction.setNodTensor3D(node, *data)

    def apply_heatflux(self, heat: np.ndarray):
        '''
        Apply the heat flux from the fluid to the solid interface
        '''

        for interaction in self.interaction_T:
            for i, data in enumerate(heat):

                node = self.FSI.getMeshPoint(i)
                interaction.setNodVector(node, *data)

    def get_position(self):
        '''
        Return the nodal positions of the solid interface
        '''

        result = np.zeros((self.get_size(), self.dim))

        for i, axe in enumerate(self.axis):
            for j, data in enumerate(result):

                node = self.FSI.getMeshPoint(j)
                data[i] += node.getValue(w.Field1D(axe, w.AB))
                data[i] += node.getValue(w.Field1D(axe, w.RE))

        return result

    def get_velocity(self):
        '''
        Return the nodal velocity of the solid interface
        '''

        result = np.zeros((self.get_size(), self.dim))

        for i, axe in enumerate(self.axis):
            for j, data in enumerate(result):

                node = self.FSI.getMeshPoint(j)
                data[i] = node.getValue(w.Field1D(axe, w.GV))

        return result

    def get_temperature(self):
        '''
        Return the nodal temperature of the solid interface
        '''

        result = np.zeros((self.get_size(), 1))

        for i in range(self.get_size()):

            node = self.FSI.getMeshPoint(i)
            result[i] += node.getValue(w.Field1D(w.TO, w.AB))
            result[i] += node.getValue(w.Field1D(w.TO, w.RE))

        return result

    def get_tempgrad(self):
        '''
        Return the nodal temperature rate of the solid interface
        '''

        result = np.zeros((self.get_size(), 1))

        for i in range(self.get_size()):

            node = self.FSI.getMeshPoint(i)
            result[i] = node.getValue(w.Field1D(w.TO, w.GV))

        return result

    def get_surface_mesh(self):
        '''
        Return the list of elements forming the polytope
        '''

        face_list = list()
        if not hasattr(self, 'polytope'): return face_list

        for elementset in self.polytope:
            face_list.append(self.get_facelist(elementset))

        return face_list

    def e_index(self, element: object):
        '''
        Split the quadangle elements into triangle elements
        '''

        size = element.getNumberOfNodes()

        if size == 2: return np.array([[1, 0]])
        if size == 3: return np.array([[2, 1, 0]])
        if size == 4: return np.array([[0, 3, 2], [2, 1, 0]])

    def get_facelist(self, elementset: object):
        '''
        Return the list of elements forming the elementset
        '''

        face_list = list()
        for i in range(elementset.size()):

            element = elementset.getElement(i)
            if not element.getEnabled(): continue

            # Split the square elements in two triangles

            position = self.e_pos(element)[self.e_index(element)]
            for pos in position: face_list.append(pos.ravel())

        return face_list

    def e_pos(self, element: object):
        '''
        Return the positions on the nodes forming the element
        '''

        size = element.getNumberOfNodes()
        position = np.zeros((size, self.dim))

        for i in range(size):

            node = element.getNodeI(i)
            for j, axe in enumerate(self.axis):

                position[i, j] += node.getValue(w.Field1D(axe, w.AB))
                position[i, j] += node.getValue(w.Field1D(axe, w.RE))

        return position

    @tb.compute_time
    def update(self):
        '''
        Store the current state of the solver into the memory
        '''

        self.meta_fac.save(self.fac)

    @tb.write_logs
    @tb.compute_time
    def way_back(self):
        '''
        Revert back the solver to its last converged FSI state
        '''

        stm = self.metafor.getStageManager()
        check_step = self.metafor.getCurrentStepNo() > self.fac.getStepNo()
        check_time = self.metafor.getLastTime() > self.metafor.getCurrentTime()

        if check_step or check_time:
            self.metafor.restart(self.fac)

        if not (stm.getCurNumStage() < 0) and (stm.getNumbOfStage() > 1):
            self.tsm.removeLastStage()

    @tb.write_logs
    @tb.compute_time
    def save(self):
        '''
        Write the current solid solution on the disk
        '''
        
        self.exporter.write()

    def get_size(self):
        '''
        Return the number of nodes on the solid interface mesh
        '''
        
        return self.FSI.getNumberOfMeshPoints()
