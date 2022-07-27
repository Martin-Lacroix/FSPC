from PIL import Image
import os

# %% Main Code

folderList = list()
workspace = os.getcwd()
workspace = os.path.join(workspace,'workspace')
background = (255,255,255)

# Lists the folders in workspace

for root,dirs,files in os.walk(workspace,topdown=False):
    for name in dirs: folderList.append(os.path.join(root,name))

# Loops over all the msh files

for folder in folderList:

    os.chdir(folder)
    for file in os.listdir():

        name,extension = os.path.splitext(file)
        if extension == '.png':

            input = Image.open(name+extension)
            input.load()

            output = Image.new("RGB",input.size,background)
            output.paste(input,mask=input.split()[3])
            output.save(name+'.pdf',quality=100,subsampling=0)