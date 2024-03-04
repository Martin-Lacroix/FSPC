from mpi4py.MPI import COMM_WORLD as CW
from ..general import Toolbox as tb
import numpy as np

# |------------------------------------|
# |   Parent FSI Interpolator Class    |
# |------------------------------------|

class Interpolator(object):
    def __init__(self):

        self.__initializeData()

        # Share the position vectors between solvers

        if CW.rank == 0:

            self.recvPos = CW.recv(source=1,tag=1)
            CW.send(tb.Solver.getPosition(),1,tag=2)

        if CW.rank == 1:

            CW.send(tb.Solver.getPosition(),0,tag=1)
            self.recvPos = CW.recv(source=0,tag=2)

# |----------------------------------------|
# |   Initialize the Interpolation Data    |
# |----------------------------------------|

    @tb.only_solid
    def __initializeData(self):

        if tb.ResMech: self.disp = tb.Solver.getPosition()
        if tb.ResTher: self.temp = tb.Solver.getTemperature()

    def initialize(self):
        raise Exception('No initialize function defined')
    
    def interpData(self):
        raise Exception('No interpolation function defined')

# |---------------------------------------|
# |   Apply the Fluid Loading on Solid    |
# |---------------------------------------|

    @tb.conv_mecha
    def applyLoadFS(self):

        if CW.rank == 0: CW.send(tb.Solver.getLoading(),1,tag=3)
        if CW.rank == 1:

            load = CW.recv(source=0,tag=3)
            tb.Solver.applyLoading(self.interpData(load))

    # Apply predicted displacement on fluid

    @tb.conv_mecha
    def applyDispSF(self):

        if CW.rank == 1: CW.send(self.disp,0,tag=4)
        if CW.rank == 0:

            disp = CW.recv(source=1,tag=4)
            tb.Solver.applyDisplacement(self.interpData(disp))

    # Apply actual heat flux on solid

    @tb.conv_therm
    def applyHeatFS(self):

        if CW.rank == 0: CW.send(tb.Solver.getHeatFlux(),1,tag=5)
        if CW.rank == 1:
            
            heat = CW.recv(source=0,tag=5)
            tb.Solver.applyHeatFlux(self.interpData(heat))

    # Apply predicted temperature on fluid

    @tb.conv_therm
    def applyTempSF(self):

        if CW.rank == 1: CW.send(self.temp,0,tag=6)
        if CW.rank == 0:
            
            temp = CW.recv(source=1,tag=6)
            tb.Solver.applyTemperature(self.interpData(temp))

# |----------------------------------------------|
# |   Predict the Solution for Next Time Step    |
# |----------------------------------------------|

    @tb.conv_mecha
    def predDisplacement(self,verified):
        
        if verified:

            self.prevDisp = np.copy(self.disp)
            self.velocityD = tb.Solver.getVelocity()

        else: self.disp = np.copy(self.prevDisp)
        self.disp += tb.Step.dt*self.velocityD

    # Predictor for the temparature coupling

    @tb.conv_therm
    def predTemperature(self,verified):

        if verified:

            self.prevTemp = np.copy(self.temp)
            self.velocityT = tb.Solver.getTempRate()

        else: self.temp = np.copy(self.prevTemp)
        self.temp += tb.Step.dt*self.velocityT

# |----------------------------------------|
# |   Send Polytope from Solid to Fluid    |
# |----------------------------------------|

    def sharePolytope(self):

        if CW.rank == 0:
            recvFace = CW.recv(source=1,tag=9)
            return recvFace

        if CW.rank == 1:
            CW.send(tb.Solver.getPolytope(),0,tag=9)
