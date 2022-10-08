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

    def printData(self,text):

        with stdout(open(self.file,'a')): print(text)
        print(text)

    def printStep(self):

        L = '\n------------------------------------------'
        timeStep = 'Time Step : {:.3e}'.format(self.algo.step.dt)
        time = '\nTime : {:.3e}'.format(self.algo.step.time).ljust(20)
        with stdout(open(self.file,'a')): print(L,time,timeStep,L)
        print(L,time,timeStep,L)
        sys.stdout.flush()

    def printRes(self):

        iter = '[{:.0f}]'.format(self.algo.iteration)
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
