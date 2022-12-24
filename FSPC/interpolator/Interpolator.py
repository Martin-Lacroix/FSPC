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
            self.disp = np.zeros((self.nbrNode,self.dim))
            com.send(self.solver.nbrNode,dest=0)

# %% Apply Actual Loading Fluid -> Solid

    def applyLoadFS(self,com):
        
        if com.rank == 1: recvLoad = np.zeros((self.recvNode,self.dim))
        if com.rank == 0: com.Send(self.solver.getLoading(),dest=1)
        if com.rank == 1:

            com.Recv(recvLoad,source=0)
            load = self.interpData(recvLoad)
            self.solver.applyLoading(load)

            # Print the transfered load in the log file

            S = np.sum((np.linalg.norm(load,axis=1)))
            F = np.sum((np.linalg.norm(recvLoad,axis=1)))
            print('Load F|S : {:.5e} - {:.5e}'.format(F,S))

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
            print('\nDisp S|F : {:.5e} - {:.5e}'.format(F,S))
