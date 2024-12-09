import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# Mesh Parameters

L = 0.2
W = 0.2
HF = 0.6
HS = 0.04
d = 0.01

# Points list

p = list()

p.append(sh.occ.addPoint(L, -W, HS, d))
p.append(sh.occ.addPoint(-L, -W, HS, d))
p.append(sh.occ.addPoint(L, -W, HS+HF, d))
p.append(sh.occ.addPoint(-L, -W, HS+HF, d))

p.append(sh.occ.addPoint(L, W, HS, d))
p.append(sh.occ.addPoint(-L, W, HS, d))
p.append(sh.occ.addPoint(L, W, HS+HF, d))
p.append(sh.occ.addPoint(-L, W, HS+HF, d))

# Lines list

l = list()

l.append(sh.occ.addLine(p[0], p[1]))
l.append(sh.occ.addLine(p[0], p[2]))
l.append(sh.occ.addLine(p[2], p[3]))
l.append(sh.occ.addLine(p[3], p[1]))

l.append(sh.occ.addLine(p[4], p[5]))
l.append(sh.occ.addLine(p[4], p[6]))
l.append(sh.occ.addLine(p[6], p[7]))
l.append(sh.occ.addLine(p[7], p[5]))

l.append(sh.occ.addLine(p[0], p[4]))
l.append(sh.occ.addLine(p[1], p[5]))
l.append(sh.occ.addLine(p[2], p[6]))
l.append(sh.occ.addLine(p[3], p[7]))

# Surfaces list

k = list()
s = list()

k.append(sh.occ.addCurveLoop([l[0], l[1], l[2], l[3]]))
k.append(sh.occ.addCurveLoop([l[7], l[6], l[5], l[4]]))
k.append(sh.occ.addCurveLoop([l[5], l[10], l[1], l[8]]))
k.append(sh.occ.addCurveLoop([l[3], l[11], l[7], l[9]]))
k.append(sh.occ.addCurveLoop([l[0], l[9], l[4], l[8]]))
k.append(sh.occ.addCurveLoop([l[6], l[11], l[2], l[10]]))

for a in k: s.append(sh.occ.addPlaneSurface([a]))
sh.occ.synchronize()

# Volumes list

h = sh.occ.addSurfaceLoop(s)
v = sh.occ.addVolume([h])
sh.occ.synchronize()

# Physical surface

sh.addPhysicalGroup(3, [v], name='Fluid')
sh.addPhysicalGroup(2, s[0:4], name='Wall')
sh.addPhysicalGroup(2, s[4:5], name='FSI')

# Mesh characteristic size

sh.mesh.field.add('Distance', 1)
sh.mesh.field.setNumber(1, 'Sampling', 1e3)
sh.mesh.field.setNumbers(1, 'SurfacesList', s[4:5])

sh.mesh.field.add('MathEval', 2)
sh.mesh.field.setString(2, 'F', f'{d}+0.05*F1')

sh.mesh.field.setAsBackgroundMesh(2)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 0)
gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary', 0)

# Write the mesh

sh.mesh.generate(3)
gmsh.write(f'{os.path.dirname(__file__)}/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()