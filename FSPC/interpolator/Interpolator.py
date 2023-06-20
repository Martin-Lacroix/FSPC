from mpi4py.MPI import COMM_WORLD as CW
from .. import Toolbox as tb
from .. import Manager as mg
import numpy as np

# %% Parent Interpolator Class

class Interpolator(object):
    def __init__(self):

        self.initInterpolator()

        # Share the position vectors between solvers

        if CW.rank == 0:

            self.recvPos = CW.recv(source=1,tag=1)
            CW.send(mg.solver.getPosition(),1,tag=2)
            self.recvNode = self.recvPos.shape[0]

        if CW.rank == 1:

            CW.send(mg.solver.getPosition(),0,tag=1)
            self.recvPos = CW.recv(source=0,tag=2)
            self.recvNode = self.recvPos.shape[0]

# %% Interpolate RecvData and Return the Result

    @tb.compute_time
    def interpData(self,recvData):
        return self.H.dot(recvData)
    
    @tb.only_solid
    def initInterpolator(self):

        if mg.convMecha: self.pos = mg.solver.getPosition()
        if mg.convTherm: self.temp = mg.solver.getTemperature()

# %% Apply Actual Loading on Solid

    @tb.only_mecha
    def applyLoadFS(self):

        if CW.rank == 0: CW.send(mg.solver.getLoading(),1,tag=3)
        if CW.rank == 1:

            load = CW.recv(source=0,tag=3)
            mg.solver.applyLoading(self.interpData(load))

# Apply predicted displacement on fluid

    @tb.only_mecha
    def applyDispSF(self):

        if CW.rank == 1: CW.send(self.pos,0,tag=4)
        if CW.rank == 0:

            pos = CW.recv(source=1,tag=4)
            mg.solver.applyPosition(self.interpData(pos))

# Apply actual heat flux on solid

    @tb.only_therm
    def applyHeatFS(self):

        if CW.rank == 0: CW.send(mg.solver.getHeatFlux(),1,tag=5)
        if CW.rank == 1:
            
            heat = CW.recv(source=0,tag=5)
            mg.solver.applyHeatFlux(self.interpData(heat))

# Apply predicted temperature on fluid

    @tb.only_therm
    def applyTempSF(self):

        if CW.rank == 1: CW.send(self.temp,0,tag=6)
        if CW.rank == 0:
            
            temp = CW.recv(source=1,tag=6)
            mg.solver.applyTemperature(self.interpData(temp))

# %% Predict the Solution for Next Time Step

    @tb.only_mecha
    def predicMecha(self,verified):

        if verified:
            
            self.prevPos = np.copy(self.pos)
            self.ratePos = mg.solver.getVelocity()

        else: self.pos = np.copy(self.prevPos)
        self.pos += mg.step.dt*self.ratePos

    # Predictor for the temparature coupling

    @tb.only_therm
    def predicTerm(self,verified):

        if verified:
            
            self.prevTemp = np.copy(self.temp)
            self.rateTemp = mg.solver.getTempVeloc()

        else: self.temp = np.copy(self.prevTemp)
        self.temp += mg.step.dt*self.rateTemp
            