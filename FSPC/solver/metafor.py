from ..general import toolbox as tb
import numpy as np
import wrap as w

# Solid solver wrapper class for Metafor

class Solver(tb.Static):
    def __init__(self, path: str):
        '''
        Initialize the solid solver wrapper class
        '''

        # Hack to load Metafor as a Python module

        import importlib.util as util

        spec = util.spec_from_file_location('module.name', path)
        module = util.module_from_spec(spec)

        # Hack to import and execute the Metafor module

        import sys

        sys.modules['module.name'] = module
        spec.loader.exec_module(module)

        # Actually initialize Metafor from a file

        parm = dict()

        object.__setattr__(self, 'metafor', module.getMetafor(parm))
        object.__setattr__(self, 'max_division', 200)

        # Copy the Metafor input dictionary into the wrapper

        self.__dict__.update(parm)
        geometry = self.metafor.getDomain().getGeometry()

        # Store important classes and variables

        object.__setattr__(self, 'dim', geometry.getDimension().getNdim())
        object.__setattr__(self, 'axis', [w.TX, w.TY, w.TZ][:self.dim])

        # Create the memory fac used to restart

        object.__setattr__(self, 'fac', w.MemoryFac())
        object.__setattr__(self, 'meta_fac', w.MetaFac(self.metafor))

        # Parameters : binary mode, zipped mode, memory mode

        self.meta_fac.mode(False, False, True)
        self.meta_fac.save(self.fac)

        # Initialize the time integration and the boundary conditions

        self.metafor.getTimeStepManager().setInitialTime(0, np.inf)
        self.metafor.getInitialConditionSet().update(0)

    @tb.write_logs
    @tb.compute_time
    def run(self):
        '''
        Run the solid solver within the current time step
        '''

        # Parameters : next final time, number of facs, initial time step

        end = tb.Step.time+tb.Step.dt
        self.metafor.getTimeStepManager().setNextTime(end, 0, tb.Step.dt)

        # The minimal time step is set by the maximum division factor

        min_dt = tb.Step.dt/self.max_division
        self.metafor.getTimeStepManager().setMinimumTimeStep(min_dt)

        # Return true if Metafor solved the time step successfully

        if self.metafor.getTimeIntegration().integration():

            self.metafor.getTimeIntegration().savePredictor()
            self.metafor.getTimeIntegration().setCustomPredictor(True)
            return True

        # Return false if Metafor failed to solve the time step

        else: return False

    def apply_loading(self, load: np.ndarray):
        '''
        Apply the loading from the fluid to the solid interface
        '''

        geometry = self.metafor.getDomain().getGeometry()

        # Loop on the mechanical interactions defined by the user

        for interaction in np.atleast_1d(self.interaction_M):
            for i, data in enumerate(load):

                node = self.FSInterface.getMeshPoint(i)

                # Axisymmetric stress tensor parameters : rr, tt, yy, ry

                if geometry.isAxisymmetric():
                    interaction.setNodTensorAxi(node, *data)

                # 2D stress tensor parameters : xx, yy, xy

                elif geometry.is2D():
                    interaction.setNodTensor2D(node, *data)

                # 3D stress tensor parameters : xx, yy, zz, xy, xz, yz

                elif geometry.is3D():
                    interaction.setNodTensor3D(node, *data)

    def apply_heatflux(self, heat: np.ndarray):
        '''
        Apply the heat flux from the fluid to the solid interface
        '''

        # Loop on the temperature interactions defined by the user

        for interaction in np.atleast_1d(self.interaction_T):
            for i, data in enumerate(heat):

                # The temperature gradient is defined in global axis

                node = self.FSInterface.getMeshPoint(i)
                interaction.setNodVector(node, *data)

    def get_position(self):
        '''
        Return the nodal positions of the solid interface
        '''

        result = np.zeros((self.dim, self.get_size()))

        # Loop on the dimensions of the mesh : TX, TY and TZ

        for i, axe in enumerate(self.axis):

            # Define a database nodal extractor for the absolute position

            field = w.Field1D(axe, w.AB)
            result[i] += w.DbNodalValueExtractor(self.FSInterface, field).extract()

            # Define a database nodal extractor for the relative position

            field = w.Field1D(axe, w.RE)
            result[i] += w.DbNodalValueExtractor(self.FSInterface, field).extract()

        # Transpose because FSPC assumes result[i] = i-th node

        return np.transpose(result)

    def get_velocity(self):
        '''
        Return the nodal velocity of the solid interface
        '''

        result = np.zeros((self.dim, self.get_size()))

        # Loop on the dimensions of the mesh : TX, TY and TZ

        for i, axe in enumerate(self.axis):

            # Define a database nodal extractor for the velocity field

            field = w.Field1D(axe, w.GV)
            result[i] = w.DbNodalValueExtractor(self.FSInterface, field).extract()

        # Transpose because FSPC assumes result[i] = i-th node

        return np.transpose(result)

    def get_temperature(self):
        '''
        Return the nodal temperature of the solid interface
        '''

        result = np.zeros((1, self.get_size()))

        # Define a database nodal extractor for the absolute temperature

        field = w.Field1D(w.TO, w.AB)
        result[0] += w.DbNodalValueExtractor(self.FSInterface, field).extract()

        # Define a database nodal extractor for the relative temperature

        field = w.Field1D(w.TO, w.RE)
        result[0] += w.DbNodalValueExtractor(self.FSInterface, field).extract()

        # Transpose because FSPC assumes result[i] = i-th node

        return np.transpose(result)

    def get_temperature_rate(self):
        '''
        Return the nodal temperature rate of the solid interface
        '''

        result = np.zeros((1, self.get_size()))

        # Define a database nodal extractor for the temperature rate

        field = w.Field1D(w.TO, w.GV)
        result[0] = w.DbNodalValueExtractor(self.FSInterface, field).extract()

        # Transpose because FSPC assumes result[i] = i-th node

        return np.transpose(result)

    @tb.compute_time
    def update(self):
        '''
        Store the current state of the solver into the memory
        '''

        self.meta_fac.save(self.fac)
        self.metafor.getTimeIntegration().setCustomPredictor(False)

    @tb.write_logs
    @tb.compute_time
    def way_back(self):
        '''
        Revert back the solver to its last converged FSI state
        '''

        # Restart if either the step or the time has advanced

        if (self.metafor.getCurrentStepNo() > self.fac.getStepNo()) or \
           (self.metafor.getLastTime() >= self.metafor.getCurrentTime()):

            self.metafor.restart(self.fac)

        # Remove the last stage if more than one stage has been stored

        if not (self.metafor.getStageManager().getCurNumStage() < 0) \
           and (self.metafor.getStageManager().getNumbOfStage() > 1):

            self.metafor.getTimeStepManager().removeLastStage()

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
        
        return self.FSInterface.getNumberOfMeshPoints()
