from ..toolbox import compute_time
from mpi4py import MPI
import numpy as np

# %% Parent Interpolator Class

class Interpolator(object):
    def __init__(self,solver):

        com = MPI.COMM_WORLD
        self.solver = solver
        self.recvNode = None

        # Number of nodes from the other process

        if com.rank == 0:

            com.send(self.solver.nbrNode,dest=1)
            self.recvNode = com.recv(self.recvNode,source=1)

        if com.rank == 1:
            
            self.recvNode = com.recv(self.recvNode,source=0)
            com.send(self.solver.nbrNode,dest=0)

    # Interpolate recvData and return the result

    @compute_time
    def interpData(self,recvData):
        return self.H.dot(recvData)

# %% Apply Actual Loading Fluid -> Solid

    def applyLoadFS(self,com):

        if com.rank == 0: com.send(self.solver.getLoading(),dest=1)
        if com.rank == 1:

            recvLoad = None
            recvLoad = com.recv(recvLoad,source=0)
            load = self.interpData(recvLoad)
            self.solver.applyLoading(load)

# %% Apply Predicted Displacement Solid -> Fluid

    def applyDispSF(self,com):

        if com.rank == 1: com.send(self.disp.copy(),dest=0)
        if com.rank == 0:

            recvDisp = None
            recvDisp = com.recv(recvDisp,source=1)
            disp = self.interpData(recvDisp)
            self.solver.applyDisplacement(disp)

# %% Apply Actual Heat Flux Fluid -> Solid

    def applyHeatFS(self,com):
        
        if com.rank == 0: com.send(self.solver.getHeatFlux(),dest=1)
        if com.rank == 1:
            
            recvHeat = None
            recvHeat = com.recv(recvHeat,source=0)
            heat = self.interpData(recvHeat)
            self.solver.applyHeatFlux(heat)

# %% Apply Predicted Temperature Solid -> Fluid

    def applyTempSF(self,com):

        if com.rank == 1: com.send(self.temp.copy(),dest=0)
        if com.rank == 0:
            
            recvTemp = None
            recvTemp = com.recv(recvTemp,source=1)
            temp = self.interpData(recvTemp)
            self.solver.applyTemperature(temp)
            