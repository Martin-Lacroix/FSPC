import numpy as np

# %% Parent Interpolator Class

class Interpolator(object):
    def __init__(self,input,com):

        self.solver = input['solver']
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

# %% Apply actual loading Fluid -> Solid

    def applyLoadFS(self,time,com):
        
        if com.rank == 1: recvLoad = np.zeros((self.recvNode,self.dim))
        if com.rank == 0: com.Send(self.solver.getLoading(),dest=1)
        if com.rank == 1:

            com.Recv(recvLoad,source=0)
            load = self.interpData(recvLoad)
            self.solver.applyLoading(load,time)

# %% Apply predicted displacement Solid -> Fluid

    def applyDispSF(self,com):

        if com.rank == 0: recvDisp = np.zeros((self.recvNode,self.dim))
        if com.rank == 1: com.Send(self.disp.copy(),dest=0)
        if com.rank == 0:

            com.Recv(recvDisp,source=1)
            disp = self.interpData(recvDisp)
            self.solver.applyDisplacement(disp)
