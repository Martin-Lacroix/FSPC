from .. import tools
import numpy as np

# %% Parent Interpolator Class

class Interpolator(object):
    def __init__(self,input,com):

        self.solver = input['solver']
        self.logGen = tools.LogGen(self)
        self.nbrNode = self.solver.nbrNode
        self.dim = self.solver.dim
        self.recvNode = None

        # Number of nodes from the other process

        if com.rank == 0:

            com.send(self.solver.nbrNode,dest=1)
            self.recvNode = com.recv(self.recvNode,source=1)

        if com.rank == 1:
            
            self.recvNode = com.recv(self.recvNode,source=0)
            self.disp = np.zeros((self.nbrNode,self.dim))
            com.send(self.solver.nbrNode,dest=0)

# %% Apply Actual Loading Fluid -> Solid

    def applyLoadFS(self,time,com):
        
        if com.rank == 1: recvLoad = np.zeros((self.recvNode,self.dim))
        if com.rank == 0: com.Send(self.solver.getLoading(),dest=1)
        if com.rank == 1:

            com.Recv(recvLoad,source=0)
            load = self.interpData(recvLoad)
            self.solver.applyLoading(load,time)

            # Print the transfered load in the log file

            S = np.mean((np.linalg.norm(load,axis=1)))
            F = np.mean((np.linalg.norm(recvLoad,axis=1)))
            self.logGen.printData('Load F|S : {:.5e} - {:.5e}'.format(F,S))

# %% Apply Predicted Displacement Solid -> Fluid

    def applyDispSF(self,com):

        if com.rank == 0: recvDisp = np.zeros((self.recvNode,self.dim))
        if com.rank == 1: com.Send(self.disp.copy(),dest=0)
        if com.rank == 0:

            com.Recv(recvDisp,source=1)
            disp = self.interpData(recvDisp)
            self.solver.applyDisplacement(disp)

            # Print the transfered load in the log file

            S = np.mean((np.linalg.norm(disp,axis=1)))
            F = np.mean((np.linalg.norm(recvDisp,axis=1)))
            self.logGen.printData('\nDisp S|F : {:.5e} - {:.5e}'.format(F,S))

# %% Check Interpolation Least Squares Error

    def checkInterp(self,com):
        
        if com.rank == 1: recvLoad = np.zeros((self.recvNode,self.dim))
        if com.rank == 0: com.Send(self.solver.getLoading(),dest=1)
        if com.rank == 1:

            com.Recv(recvLoad,source=0)
            load = self.interpData(recvLoad)

        # Interpolate-back the load on the fluid

        if com.rank == 0: recvLoad = np.zeros((self.recvNode,self.dim))
        if com.rank == 1: com.Send(load.copy(),dest=0)
        if com.rank == 0:
            
            interpLoad = None
            com.Recv(recvLoad,source=1)
            interpLoad = self.interpData(recvLoad)
            load = self.solver.getLoading()

            # Compute the average relative error

            normF = np.linalg.norm(load,axis=1)
            normS = np.linalg.norm(interpLoad,axis=1)
            error = np.trapz(np.power(normF-normS,2))

            normF = np.trapz(normF**2)
            error = np.divide(error,normF,where=(normF!=0))

            self.logGen.printData('Interp Error : {:.6e}'.format(error))
            self.logGen.printData('------------------------------------------')
