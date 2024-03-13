import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

d = 2e-3
RS = 0.0125
HS = 0.014
HF = 0.05

# Volumes List

v = sh.occ.addSphere(0, 0, HS + HF, RS)
sh.occ.synchronize()

g = sh.getBoundary([(3, v)], 0, 0, 0)[0][1]
p = sh.getBoundary([(3, v)], 0, 0, 1)
sh.mesh.setSize(p, d)
sh.occ.synchronize()

# Physical Surface

sh.addPhysicalGroup(3, [v], name='Solid')
sh.addPhysicalGroup(2, [g], name='FSInterface')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(3)
gmsh.write(os.path.dirname(__file__) + '/geometry_S.msh')
gmsh.fltk.run()
gmsh.finalize()
