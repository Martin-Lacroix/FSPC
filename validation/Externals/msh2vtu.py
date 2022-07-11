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
    for file in os.listdir():

        name,extension = os.path.splitext(file)
        if extension == '.msh':

            name = name[:15]
            msh = meshio.read(file)
            name = name.replace('.','')
            meshio.write(name+'.vtu',msh,file_format='vtu')