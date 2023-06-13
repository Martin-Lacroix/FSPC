from mpi4py.MPI import COMM_WORLD as CW
from .. import Toolbox as tb

# %% Parent Interpolator Class

class Interpolator(object):
    def __init__(self,solver):

        self.solver = solver
        self.H = tb.Undefined()

        # Share the position vectors between solvers

        if CW.rank == 0:

            self.recvPos = CW.recv(source=1,tag=1)
            CW.send(self.solver.getPosition(),1,tag=2)
            self.recvNode = self.recvPos.shape[0]

        if CW.rank == 1:

            CW.send(self.solver.getPosition(),0,tag=1)
            self.recvPos = CW.recv(source=0,tag=2)
            self.recvNode = self.recvPos.shape[0]

    # Interpolate recvData and return the result

    @tb.compute_time
    def interpData(self,recvData):
        return self.H.dot(recvData)

# %% Apply Actual Loading Fluid -> Solid

    def applyLoadFS(self):

        if CW.rank == 0: CW.send(self.solver.getLoading(),1,tag=3)
        if CW.rank == 1:

            load = CW.recv(source=0,tag=3)
            self.solver.applyLoading(self.interpData(load))

# %% Apply Predicted Displacement Solid -> Fluid

    def applyDispSF(self,dt):

        if CW.rank == 1: CW.send(self.pos,0,tag=4)
        if CW.rank == 0:

            pos = CW.recv(source=1,tag=4)
            self.solver.applyPosition(self.interpData(pos),dt)

# %% Apply Actual Heat Flux Fluid -> Solid

    def applyHeatFS(self):

        if CW.rank == 0: CW.send(self.solver.getHeatFlux(),1,tag=5)
        if CW.rank == 1:
            
            heat = CW.recv(source=0,tag=5)
            self.solver.applyHeatFlux(self.interpData(heat))

# %% Apply Predicted Temperature Solid -> Fluid

    def applyTempSF(self):

        if CW.rank == 1: CW.send(self.temp,0,tag=6)
        if CW.rank == 0:
            
            temp = CW.recv(source=1,tag=6)
            self.solver.applyTemperature(self.interpData(temp))
            