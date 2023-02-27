import numpy as np
import meshio
import os

# %% Main Code

folderList = list()
workspace = os.getcwd()
workspace = os.path.join(workspace,'workspace')

# Lists the folders in workspace

for root,dirs,files in os.walk(workspace,topdown=False):
    for name in dirs: folderList.append(os.path.join(root,name))

# Loops over all the msh files

for folder in folderList:

    os.chdir(folder)
    file = os.listdir()
    time = np.zeros(len(file))

    # Sort the output files

    for i,F in enumerate(file):

        fileName = os.path.splitext(F)[0]
        time[i] = float(fileName[fileName.index('_')+1:])

    index = np.argsort(time)
    file = [file[i] for i in index]

    # Rename and convert the files

    for i,F in enumerate(file):

        msh = meshio.gmsh.read(F)
        fileName = 'file_'+str(i)+'.vtu'
        meshio.write(fileName,msh,file_format='vtu')