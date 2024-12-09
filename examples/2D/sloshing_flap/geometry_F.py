import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# Mesh Parameters

L = 0.609/2
H = 0.3445
LS = 0.004/2
HS = 0.1148

d = 5e-3

# Points list

p = list()

p.append(sh.occ.addPoint(-L, 0, 0, d))
p.append(sh.occ.addPoint(L, 0, 0, d))
p.append(sh.occ.addPoint(L, HS, 0, d))
p.append(sh.occ.addPoint(L, H, 0, d))
p.append(sh.occ.addPoint(-L, H, 0, d))
p.append(sh.occ.addPoint(-L, HS, 0, d))

p.append(sh.occ.addPoint(L, 0, 0, d))
p.append(sh.occ.addPoint(-LS, 0, 0, d))
p.append(sh.occ.addPoint(-LS, HS, 0, d))
p.append(sh.occ.addPoint(LS, HS, 0, d))
p.append(sh.occ.addPoint(LS, 0, 0, d))

# Lines list

l = list()
h = list()

l.append(sh.occ.addLine(p[8], p[5]))
l.append(sh.occ.addLine(p[5], p[0]))
l.append(sh.occ.addLine(p[0], p[7]))
l.append(sh.occ.addLine(p[7], p[8]))

l.append(sh.occ.addLine(p[9], p[10]))
l.append(sh.occ.addLine(p[10], p[1]))
l.append(sh.occ.addLine(p[1], p[2]))
l.append(sh.occ.addLine(p[2], p[9]))

l.append(sh.occ.addLine(p[8], p[9]))
l.append(sh.occ.addLine(p[4], p[5]))
l.append(sh.occ.addLine(p[2], p[3]))

# Physical surface

s = list()

k = sh.occ.addCurveLoop(l[0:4])
s.append(sh.occ.addPlaneSurface([k]))

k = sh.occ.addCurveLoop(l[4:8])
s.append(sh.occ.addPlaneSurface([k]))

sh.occ.synchronize()

# Physical boundary

sh.addPhysicalGroup(2, s, name='Fluid')
sh.addPhysicalGroup(1, l[3:5]+l[8:9], name='FSI')
sh.addPhysicalGroup(1, l[1:3]+l[5:7]+l[9:11], name='Container')

# Mesh characteristic size

sh.mesh.field.add('Distance', 1)
sh.mesh.field.setNumber(1, 'Sampling', 1e4)
sh.mesh.field.setNumbers(1, 'CurvesList', l)

sh.mesh.field.add('MathEval', 2)
sh.mesh.field.setString(2, 'F', f'{d}+0.1*F1')

sh.mesh.field.setAsBackgroundMesh(2)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 0)
gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary', 0)

# Write the mesh

sh.mesh.generate(2)
gmsh.write(f'{os.path.dirname(__file__)}/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()