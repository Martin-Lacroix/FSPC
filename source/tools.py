from contextlib import redirect_stdout as stdout
import numpy as np
import time
import sys

# %% Simulation Timer Class

class Clock(object):

    def __init__(self):

        self.time = 0
        self.begin = 0
        self.run = False

    def start(self):
            
        if self.run: raise Exception('The clock is already running')
        self.begin = time.time()
        self.run = True

    def end(self):

        if not self.run: raise Exception('The clock is not running')
        self.time += time.time()-self.begin
        self.run = False

# %% Redirecting Prints to Files

class Log(object):

    def __init__(self,file):
        self.file = file

    def exec(self,function,*args):
            
        with open(self.file,'a') as F:
            with stdout(F): output = function(*args)
        return output

# %% General Print and Log File

class LogGen(object):

    def __init__(self,algorithm):

        self.file = 'general.log'
        self.algo = algorithm

    def printStep(self):

        time = '\nTime : {:.3e}'.format(self.algo.step.time).ljust(20)
        timeStep = 'Time Step : {:.3e}'.format(self.algo.step.dt)
        with stdout(open(self.file,'a')): print(time,timeStep)
        print(time,timeStep)
        sys.stdout.flush()

    def printRes(self):

        iter = 'Iteration : {:.0f}'.format(self.algo.iteration).ljust(20)
        epsilon = 'Residual : {:.3e}'.format(self.algo.converg.epsilon)
        with stdout(open(self.file,'a')): print(iter,epsilon)
        print(iter,epsilon)
        sys.stdout.flush()

    def printClock(self,com):
        
        clock = self.algo.clock
        total = clock['Total Time'].time/100
        text = '\nRank {:.0f} Time Stats\n'.format(com.rank)

        for key,value in clock.items():
            
            text += '\n{} '.format(key).ljust(25,'-')
            text += ' {:.5f} '.format(value.time).ljust(20,'-')
            text += ' {:.3f} %'.format(value.time/total)

        print(text)
        with stdout(open(self.file,'a')): print(text)
        sys.stdout.flush()

# %% MPI Transfer Functions

def scatterSF(data,com):

    data = np.atleast_1d(data)
    if com.rank == 0: data = np.zeros(1,dtype=int)
    if com.rank == 1: com.Send(data.copy(),dest=0)
    if com.rank == 0: com.Recv(data,source=1)
    return data[0]

def scatterFS(data,com):

    data = np.atleast_1d(data)
    if com.rank == 1: data = np.zeros(1,dtype=int)
    if com.rank == 0: com.Send(data.copy(),dest=1)
    if com.rank == 1: com.Recv(data,source=0)
    return data[0]




















# %% Testings

import numpy as np

def QRfiltering_mod(V, W, toll):
    
    while True:
        n = V.shape[0]
        s = V.shape[1]
        Q = np.zeros((n, s))
        R = np.zeros((s, s))
        
        flag = True
        
        i = 0
        V0 = V[:,i]
        R[i,i] = np.linalg.norm(V0, 2)
        Q[:,i] = np.dot(V0, 1.0/R[i,i])
        
        for i in range(1, s): # REMEMBER: range(a, b) starts at a but ends at b-1!
            vbar = V[:,i]
            for j in range(0, i): # REMEMBER: range(a, b) starts at a but ends at b-1!
                R[j,i] = np.dot(Q[:,j].T,vbar)
                vbar = vbar - np.dot(Q[:,j], R[j,i])
            if np.linalg.norm(vbar, 2) < toll*np.linalg.norm(V[:,i], 2):
                V = np.delete(V, i, 1)
                W = np.delete(W, i, 1)
                if i == s-1:
                    flag = False
                else:
                    flag = True
                break
            else:
                R[i,i] = np.linalg.norm(vbar, 2)
                Q[:,i] = np.dot(vbar, 1.0/R[i,i])
        if i >= s-1 and flag == True:
            return (Q, R, V, W)

def qrSolve(V,W,res):

    tollQR = 1.0e-1
    
    # Solves with the Haelterman algorithm
    
    Q, R, V, W = QRfiltering_mod(V, W, tollQR)
    s = np.dot(np.transpose(Q), -res)
    c = np.linalg.solve(R, s)
    return c, W