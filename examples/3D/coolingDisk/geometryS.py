import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# %% Parameters

d = 2e-3
RS = 0.0125
HS = 0.014
HF = 0.05

# %% Solid Volume

v = sh.occ.addSphere(0,0,HS+HF,RS)
sh.occ.synchronize()

g = gmsh.model.getBoundary([(3,v)],0,0,0)[0][1]
p = gmsh.model.getBoundary([(3,v)],0,0,1)
sh.mesh.setSize(p,d)
sh.occ.synchronize()

# %% Physical Surface

sh.addPhysicalGroup(3,[v],name='Solid')
sh.addPhysicalGroup(2,[g],name='FSInterface')

# %% Save the Mesh

sh.mesh.generate(3)
gmsh.option.setNumber('Mesh.Binary',1)
gmsh.write(os.path.dirname(__file__)+'/geometryS.msh')
gmsh.fltk.run()
gmsh.finalize()
