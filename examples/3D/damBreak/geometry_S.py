import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

S = 0.15
L = 0.146
R = 0.015
A = 2*L

# Characteristic size

d = 0.005

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(A, -R, 0, d))
p.append(sh.occ.addPoint(A, 0, 0, d))
p.append(sh.occ.addPoint(A, R, 0, d))

p.append(sh.occ.addPoint(A, -R, S, d))
p.append(sh.occ.addPoint(A, 0, S, d))
p.append(sh.occ.addPoint(A, R, S, d))

# Lines list

l = list()

l.append(sh.occ.addLine(p[3], p[0]))
l.append(sh.occ.addLine(p[5], p[2]))

l.append(sh.occ.addCircleArc(p[0], p[1], p[2]))
l.append(sh.occ.addCircleArc(p[2], p[1], p[0]))

l.append(sh.occ.addCircleArc(p[3], p[4], p[5]))
l.append(sh.occ.addCircleArc(p[5], p[4], p[3]))

# |--------------------------------------|
# |   Surfaces and Volumes Definition    |
# |--------------------------------------|

k = list()
s = list()
g = list()

k.append(sh.occ.addCurveLoop([l[2], l[3]]))
k.append(sh.occ.addCurveLoop([-l[4], -l[5]]))
g.append(sh.occ.addCurveLoop([l[0], l[3], l[1], l[5]]))
g.append(sh.occ.addCurveLoop([l[1], l[2], l[0], l[4]]))

for a in k: s.append(sh.occ.addPlaneSurface([a]))
for a in g: s.append(sh.occ.addBSplineFilling(a))
sh.occ.synchronize()

# Volumes list

h = sh.occ.addSurfaceLoop(s)
v = sh.occ.addVolume([h])
sh.occ.synchronize()

# Physical surface

sh.addPhysicalGroup(3, [v], name='Solid')
sh.addPhysicalGroup(2, s[1:], name='FSInterface')
sh.addPhysicalGroup(2, s[0:1], name='Clamped')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(3)
gmsh.write(os.path.dirname(__file__)+'/geometry_S.msh')
gmsh.fltk.run()
gmsh.finalize()