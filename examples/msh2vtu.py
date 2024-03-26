import numpy as np
import meshio
import os

# |-------------------------------------|
# |   Convert MSH Files to VTU Files    |
# |-------------------------------------|

workspace = os.getcwd()
folderList = ['metafor', 'pfem']
workspace = os.path.join(workspace, 'workspace/')
folderList = [workspace+F for F in folderList]

# Loops over all the msh files

for folder in folderList:

    os.chdir(folder)
    file = os.listdir()
    time = np.zeros(len(file))

    # Sort the output files

    for i, F in enumerate(file):

        fileName = os.path.splitext(F)[0]
        time[i] = float(fileName[fileName.index('_')+1:])

    index = np.argsort(time)
    file = [file[i] for i in index]

    # Rename and convert the files

    for i, F in enumerate(file):

        if 'msh' not in F: break
        msh = meshio.gmsh.read(F)
        fileName = 'convert_'+str(i)+'.vtu'
        meshio.write(fileName, msh, file_format='vtu')