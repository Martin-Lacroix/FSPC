import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# Mesh Parameters

L = 1
HF = 0.2
HS = 0.02
d = 0.05

# Points list

p = list()

p.append(sh.occ.addPoint(L, HS, 0, d))
p.append(sh.occ.addPoint(0, HS, 0, d))
p.append(sh.occ.addPoint(L, HS+HF, 0, d))
p.append(sh.occ.addPoint(0, HS+HF, 0, d))

# Lines list

l = list()

l.append(sh.occ.addLine(p[0], p[1]))
l.append(sh.occ.addLine(p[0], p[2]))
l.append(sh.occ.addLine(p[2], p[3]))
l.append(sh.occ.addLine(p[3], p[1]))

# Physical surface

k = sh.occ.addCurveLoop(l)
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

# Physical boundary

sh.addPhysicalGroup(2, [s], name='Fluid')
sh.addPhysicalGroup(1, l[0:1], name='FSI')
sh.addPhysicalGroup(1, l[1:2]+l[3:4], name='Wall')

# Write the mesh file

sh.mesh.generate(2)
gmsh.model.mesh.reverse()
gmsh.write(f'{os.path.dirname(__file__)}/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()