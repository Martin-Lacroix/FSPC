from ..toolbox import compute_time
import numpy as np

# %% Parent Interpolator Class

class Interpolator(object):
    def __init__(self,solver,com):

        self.solver = solver
        self.dim = self.solver.dim
        self.nbrNode = self.solver.nbrNode
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

            # Print the transfered load in the log file

            S = np.mean((np.linalg.norm(load,axis=1)))
            F = np.mean((np.linalg.norm(recvLoad,axis=1)))
            print('Load F|S : {:.5e} - {:.5e}'.format(F,S))

# %% Apply Predicted Displacement Solid -> Fluid

    def applyDispSF(self,com):

        if com.rank == 1: com.send(self.disp.copy(),dest=0)
        if com.rank == 0:

            recvDisp = None
            recvDisp = com.recv(recvDisp,source=1)
            disp = self.interpData(recvDisp)
            self.solver.applyDisplacement(disp)

            # Print the transfered load in the log file

            S = np.mean((np.linalg.norm(disp,axis=1)))
            F = np.mean((np.linalg.norm(recvDisp,axis=1)))
            print('\nDisp S|F : {:.5e} - {:.5e}'.format(F,S))

# %% Apply Actual Heat Flux Fluid -> Solid

    def applyHeatFS(self,com):
        
        if com.rank == 0: com.send(self.solver.getHeatFlux(),dest=1)
        if com.rank == 1:
            
            recvHeat = None
            recvHeat = com.recv(recvHeat,source=0)
            heat = self.interpData(recvHeat)
            self.solver.applyHeatFlux(heat)

            # Print the transfered load in the log file

            S = np.mean((np.linalg.norm(heat,axis=1)))
            F = np.mean((np.linalg.norm(recvHeat,axis=1)))
            print('Flux F|S : {:.5e} - {:.5e}'.format(F,S))

# %% Apply Predicted Temperature Solid -> Fluid

    def applyTempSF(self,com):

        if com.rank == 1: com.send(self.temp.copy(),dest=0)
        if com.rank == 0:
            
            recvTemp = None
            recvTemp = com.recv(recvTemp,source=1)
            temp = self.interpData(recvTemp)
            self.solver.applyTemperature(temp)

            # Print the transfered load in the log file

            S = np.mean((np.linalg.norm(temp,axis=1)))
            F = np.mean((np.linalg.norm(recvTemp,axis=1)))
            print('\nTemp S|F : {:.5e} - {:.5e}'.format(F,S))
            