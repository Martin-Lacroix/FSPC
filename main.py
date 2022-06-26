import argparse
import sys
import os








import mpi4py.MPI as mpi

com = mpi.COMM_WORLD






# %% Solver Paths

parentFolder = os.path.dirname(os.getcwd())
sys.path.append(parentFolder+'/Metafor/Metafor')
sys.path.append(parentFolder+'/Metafor/oo_meta')
sys.path.append(parentFolder+'/PFEM3D/build/bin')
sys.path.append(parentFolder+'/Metafor/build/bin')

# %% Terminal and Paths

parser = argparse.ArgumentParser()
parser.add_argument('file',nargs=1,help='Python input file')
parser.add_argument('-k',nargs=1,help='Number of threads')
file = parser.parse_args().file[0]

# Stores some useful paths

baseFolder = os.getcwd()
inputFile = os.path.abspath(file)
inputFolder = os.path.dirname(inputFile)
sys.path.append(inputFolder)

# Makes the workspace

workspace = os.path.basename(inputFolder)
workspace = os.path.join(baseFolder,'workspace',workspace)

if(com.rank == 0):
    if not os.path.isdir(workspace): os.makedirs(workspace)

com.Barrier()

os.chdir(workspace)

# %% Runs the simulation

import importlib
import source.master as FSPC

module = os.path.splitext(os.path.basename(inputFile))[0]
module = importlib.import_module(module)

param = module.getParam(inputFolder)
master = FSPC.Master(param,com)
master.algo.run(com)


com.Barrier()
print('\nRank = ',com.rank,'- END\n')