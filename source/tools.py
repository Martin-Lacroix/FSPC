import time

# %% Coloured Print

def printY(*text): print('\033[33m'); print(*text,'\033[0m')
def printB(*text): print('\033[96m'); print(*text,'\033[0m')
def printG(*text): print('\033[92m'); print(*text,'\033[0m')

# %% Prints the computation time stats

def timerPrint(clock):

    printG('FSPC Time Stats\n')
    total = clock['Total time'].time

    for key,value in clock.items():

        time = ' {:.5f} '.format(value.time)
        percent = ' {:.3f} %'.format(value.time/total*100)
        print((str(key)+' ').ljust(25,'-')+time.ljust(20,'-')+percent)

# %% Write Output

class Logs(object):
    def __init__(self,file,data):

        self.file = file
        self.data = data

    # Writes an empty line

    def newLine(self):
        with open(self.file,'a') as f: f.write('\n')

    # Writes a line of logs

    def write(self,*input):

        f = open(self.file,'a')
        for i in range(len(input)):

            text = self.data[i]+' : '
            if isinstance(input[i],int): text += str(input[i])
            else: text += '{:.3e}'.format(input[i])
            f.write(text.ljust(20))

        f.write('\n')
        f.close()

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









# %% MPI Transfer Functions

def scatterSF(data,com):

        if com.rank == 0: data = None
        if com.rank == 1: data = np.repeat(data,2)
        data = com.scatter(data,root=1)
        return data


def scatterFS(data,com):

        if com.rank == 1: data = None
        if com.rank == 0: data = np.repeat(data,2)
        data = com.scatter(data,root=0)
        return data