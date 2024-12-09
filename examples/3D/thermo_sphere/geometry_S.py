import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# Mesh Parameters

d = 2e-3
RS = 0.0125
HS = 0.014
HF = 0.05

# Volumes list

v = sh.occ.addSphere(0, 0, HS+HF, RS)
sh.occ.synchronize()

g = sh.getBoundary([(3, v)], 0, 0, 0)[0][1]
p = sh.getBoundary([(3, v)], 0, 0, 1)
sh.mesh.setSize(p, d)
sh.occ.synchronize()

# Physical surface

sh.addPhysicalGroup(3, [v], name='Solid')
sh.addPhysicalGroup(2, [g], name='FSI')

# Write the mesh file

sh.mesh.generate(3)
gmsh.write(f'{os.path.dirname(__file__)}/geometry_S.msh')
gmsh.fltk.run()
gmsh.finalize()
