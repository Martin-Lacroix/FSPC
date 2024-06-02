from ..general import toolbox as tb
import importlib.util as util
import numpy as np
import wrap as w
import sys

# |---------------------------------------|
# |   Solid Solver Wrapper for Metafor    |
# |---------------------------------------|

class Metafor(tb.Frozen):
    def __init__(self, path: str):

        # Convert Metafor into a module

        parm = dict()
        spec = util.spec_from_file_location('module.name', path)
        module = util.module_from_spec(spec)
        sys.modules['module.name'] = module
        spec.loader.exec_module(module)

        # Actually initialize Metafor from file

        self.__setattr__('metafor', module.getMetafor(parm))
        self.__setattr__('max_division', 200)

        self.__dict__.update(parm)
        self.__dict__['FSI'] = self.__dict__.pop('FSInterface')

        # Defines some internal variables

        self.__setattr__('geometry', self.metafor.getDomain().getGeometry())
        self.__setattr__('dim', self.geometry.getDimension().getNdim())
        self.__setattr__('tsm', self.metafor.getTimeStepManager())

        # Sets the dimension of the interaction

        if self.dim == 2: self.__setattr__('axis', (w.TX, w.TY))
        if self.dim == 3: self.__setattr__('axis', (w.TX, w.TY, w.TZ))

        # Create the memory fac used to restart

        self.__setattr__('fac', w.MemoryFac())
        self.__setattr__('meta_fac', w.MetaFac(self.metafor))

        self.meta_fac.mode(False, False, True)
        self.meta_fac.save(self.fac)

        # Initialize the integration and restart

        self.tsm.setInitialTime(0, np.inf)
        self.metafor.getInitialConditionSet().update(0)

        tb.Frozen.__init__(self)

# |--------------------------------------------|
# |   Run Metafor in the Current Time Frame    |
# |--------------------------------------------|

    @tb.write_logs
    @tb.compute_time
    def run(self):

        self.tsm.setNextTime(tb.Step.next_time(), 0, tb.Step.dt)
        self.tsm.setMinimumTimeStep(tb.Step.dt/self.max_division)
        return self.metafor.getTimeIntegration().integration()

# |----------------------------------|
# |   Neumann Boundary Conditions    |
# |----------------------------------|

    def apply_loading(self, load: np.ndarray):

        for interaction in np.atleast_1d(self.interaction_M):
            for i, data in enumerate(load):

                node = self.FSI.getMeshPoint(i)

                if self.geometry.isAxisymmetric():
                    interaction.setNodTensorAxi(node, *data)

                elif self.geometry.is2D():
                    interaction.setNodTensor2D(node, *data)

                elif self.geometry.is3D():
                    interaction.setNodTensor3D(node, *data)

    # Apply Thermal boundary conditions

    def apply_heatflux(self, heat: np.ndarray):

        for interaction in np.atleast_1d(self.interaction_T):
            for i, data in enumerate(heat):

                node = self.FSI.getMeshPoint(i)
                interaction.setNodVector(node, *data)

# |-------------------------------------|
# |   Return Mechanical Nodal Values    |
# |-------------------------------------|

    def get_position(self):

        result = np.zeros((self.get_size(), self.dim))

        for i, axe in enumerate(self.axis):
            for j, data in enumerate(result):

                node = self.FSI.getMeshPoint(j)
                data[i] += node.getValue(w.Field1D(axe, w.AB))
                data[i] += node.getValue(w.Field1D(axe, w.RE))

        return result

    # Computes the nodal velocity result

    def get_velocity(self):

        result = np.zeros((self.get_size(), self.dim))

        for i, axe in enumerate(self.axis):
            for j, data in enumerate(result):

                node = self.FSI.getMeshPoint(j)
                data[i] = node.getValue(w.Field1D(axe, w.GV))

        return result

# |----------------------------------|
# |   Return Thermal Nodal Values    |
# |----------------------------------|

    def get_temperature(self):

        result = np.zeros((self.get_size(), 1))

        for i in range(self.get_size()):

            node = self.FSI.getMeshPoint(i)
            result[i] += node.getValue(w.Field1D(w.TO, w.AB))
            result[i] += node.getValue(w.Field1D(w.TO, w.RE))

        return result

    # Computes the nodal temperature velocity

    def get_tempgrad(self):

        result = np.zeros((self.get_size(), 1))

        for i in range(self.get_size()):

            node = self.FSI.getMeshPoint(i)
            result[i] = node.getValue(w.Field1D(w.TO, w.GV))

        return result

# |--------------------------------------------|
# |   Build the Facet List of the Polytopes    |
# |--------------------------------------------|

    def get_surface_mesh(self):

        face_list = list()
        if not hasattr(self, 'polytope'): return face_list

        for elementset in np.atleast_1d(self.polytope):
            face_list.append(self.get_facelist(elementset))

        return face_list

    # Correct element node ordering for PFEM3D

    def e_index(self, element: object):

        size = element.getNumberOfNodes()

        if size == 2: return np.array([[1, 0]])
        if size == 3: return np.array([[2, 1, 0]])
        if size == 4: return np.array([[0, 3, 2], [2, 1, 0]])

# |--------------------------------------------|
# |   Build the Face List of an Element Set    |
# |--------------------------------------------|

    def get_facelist(self, elementset: object):

        face_list = list()
        for i in range(elementset.size()):

            element = elementset.getElement(i)
            if not element.getEnabled(): continue

            # Split the square elements in two triangles

            position = self.e_pos(element)[self.e_index(element)]
            for pos in position: face_list.append(pos.ravel())

        return face_list

# |-------------------------------------------|
# |   Positions of the Nodes in an Element    |
# |-------------------------------------------|

    def e_pos(self, element: object):

        size = element.getNumberOfNodes()
        position = np.zeros((size, self.dim))

        for i in range(size):

            node = element.getNodeI(i)
            for j, axe in enumerate(self.axis):

                position[i, j] += node.getValue(w.Field1D(axe, w.AB))
                position[i, j] += node.getValue(w.Field1D(axe, w.RE))

        return position

# |------------------------------------|
# |   Other Miscellaneous Functions    |
# |------------------------------------|

    @tb.compute_time
    def update(self): self.meta_fac.save(self.fac)

    # Backup the solver state if needed

    @tb.write_logs
    @tb.compute_time
    def way_back(self):

        check_step = self.metafor.getCurrentStepNo() > self.fac.getStepNo()
        check_time = self.metafor.getLastTime() > self.metafor.getCurrentTime()

        if check_step or check_time:
            self.metafor.restart(self.fac)

        stm = self.metafor.getStageManager()
        check_stage = stm.getNumbOfStage()-stm.getCurNumStage() > 1

        if not (stm.getCurNumStage() < 0) and check_stage:
            self.tsm.removeLastStage()

    # Export the current solution into a file

    @tb.write_logs
    @tb.compute_time
    def save(self): self.exporter.write()

    # Return the number of nodes at the interface

    def get_size(self): return self.FSI.getNumberOfMeshPoints()
