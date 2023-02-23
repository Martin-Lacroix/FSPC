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

        name,extension = os.path.splitext(F)
        if extension == '.msh':
            time[i] = float(name[name.index('_')+1:])

    index = np.argsort(time)
    file = [file[i] for i in index]

    # Rename and convert the files

    for i,F in enumerate(file):

        name,extension = os.path.splitext(F)
        if extension == '.msh':

            msh = meshio.read(F)
            name = 'file_'+str(i)
            meshio.write(name+'.vtu',msh,file_format='vtu')