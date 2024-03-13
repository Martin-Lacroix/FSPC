from ..general import toolbox as tb
import importlib.util as util
import numpy as np
import wrap as w
import sys

# |-----------------------------------|
# |   Initializes the Solid Wraper    |
# |-----------------------------------|

class Metafor(object):
    def __init__(self, path: str):

        # Convert Metafor into a module

        parm = dict()
        spec = util.spec_from_file_location('module.name', path)
        module = util.module_from_spec(spec)
        sys.modules['module.name'] = module
        spec.loader.exec_module(module)

        # Actually initialize Metafor from file

        self.metafor = module.getMetafor(parm)
        self.geometry = self.metafor.getDomain().getGeometry()
        self.dim = self.geometry.getDimension().getNdim()
        self.tsm = self.metafor.getTimeStepManager()

        # Sets the dimension of the interaction

        if self.dim == 2: self.axis = (w.TX, w.TY)
        if self.dim == 3: self.axis = (w.TX, w.TY, w.TZ)

        # Defines some internal variables

        self.FSI = parm['FSInterface']
        self.extractor = parm['extractor']

        # Mechanical and thermal interactions

        if 'polytope' in parm:
            self.polytope = np.atleast_1d(parm['polytope'])
        else: self.polytope = list()

        if 'interaction_M' in parm:
            self.interaction_M = np.atleast_1d(parm['interaction_M'])
        else: self.interaction_M = list()

        if 'interaction_T' in parm:
            self.interaction_T = np.atleast_1d(parm['interaction_T'])
        else: self.interaction_T = list()

        # Create the memory fac used to restart

        self.fac = w.MemoryFac()
        self.meta_fac = w.MetaFac(self.metafor)
        self.meta_fac.mode(False, False, True)
        self.meta_fac.save(self.fac)

        # Initialize the integration and restart

        self.max_division = 200
        self.tsm.setInitialTime(0, np.inf)
        self.metafor.getInitialConditionSet().update(0)

# |--------------------------------------------|
# |   Run Metafor in the Current Time Frame    |
# |--------------------------------------------|

    @tb.write_logs
    @tb.compute_time
    def run(self):

        self.tsm.setNextTime(tb.Step.next_time(), 0, tb.Step.dt)
        self.tsm.setMinimumTimeStep(tb.Step.dt/self.max_division)
        return self.metafor.getTimeIntegration().restart(self.fac)

# |----------------------------------|
# |   Neumann Boundary Conditions    |
# |----------------------------------|

    def apply_loading(self, load: np.ndarray):

        for interaction in self.interaction_M:
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

        for interaction in self.interaction_T:
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

# |------------------------------|
# |   Other Wrapper Functions    |
# |------------------------------|

    @tb.compute_time
    def update(self): self.meta_fac.save(self.fac)

    @tb.write_logs
    @tb.compute_time
    def save(self): self.extractor.extract()
    def get_size(self): return self.FSI.getNumberOfMeshPoints()

    @tb.write_logs
    def exit(self): return
    def way_back(self): self.tsm.removeLastStage()

# |--------------------------------------------|
# |   Build the Facet List of the Polytopes    |
# |--------------------------------------------|

    def get_polytope(self):

        face_list = list()
        for elementset in self.polytope:
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
