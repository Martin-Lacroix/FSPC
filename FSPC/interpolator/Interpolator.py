from ..Toolbox import compute_time
from mpi4py import MPI

# %% Parent Interpolator Class

class Interpolator(object):
    def __init__(self,solver):

        com = MPI.COMM_WORLD
        self.solver = solver

        # Share the position vectors between solvers

        if com.rank == 0:

            self.recvPos = com.recv(source=1,tag=1)
            com.send(self.solver.getPosition(),1,tag=2)
            self.recvNode = self.recvPos.shape[0]

        if com.rank == 1:

            com.send(self.solver.getPosition(),0,tag=1)
            self.recvPos = com.recv(source=0,tag=2)
            self.recvNode = self.recvPos.shape[0]

    # Interpolate recvData and return the result

    @compute_time
    def interpData(self,recvData):
        return self.H.dot(recvData)

# %% Apply Actual Loading Fluid -> Solid

    def applyLoadFS(self,com):

        if com.rank == 0: com.send(self.solver.getLoading(),1,tag=3)
        if com.rank == 1:

            load = com.recv(source=0,tag=3)
            self.solver.applyLoading(self.interpData(load))

# %% Apply Predicted Displacement Solid -> Fluid

    def applyDispSF(self,dt,com):

        if com.rank == 1: com.send(self.disp,0,tag=4)
        if com.rank == 0:

            disp = com.recv(source=1,tag=4)
            self.solver.applyDisplacement(self.interpData(disp),dt)

# %% Apply Actual Heat Flux Fluid -> Solid

    def applyHeatFS(self,com):

        if com.rank == 0: com.send(self.solver.getHeatFlux(),1,tag=5)
        if com.rank == 1:
            
            heat = com.recv(source=0,tag=5)
            self.solver.applyHeatFlux(self.interpData(heat))

# %% Apply Predicted Temperature Solid -> Fluid

    def applyTempSF(self,com):

        if com.rank == 1: com.send(self.temp,0,tag=6)
        if com.rank == 0:
            
            temp = com.recv(source=1,tag=6)
            self.solver.applyTemperature(self.interpData(temp))
            