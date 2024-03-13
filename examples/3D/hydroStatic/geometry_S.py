import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

L = 1
W = 1
HS = 0.02

# Characteristic size

M = 11
N = 1

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(L, 0, 0))
p.append(sh.occ.addPoint(0, 0, 0))
p.append(sh.occ.addPoint(L, 0, HS))
p.append(sh.occ.addPoint(0, 0, HS))

p.append(sh.occ.addPoint(L, W, 0))
p.append(sh.occ.addPoint(0, W, 0))
p.append(sh.occ.addPoint(L, W, HS))
p.append(sh.occ.addPoint(0, W, HS))

# Lines List

l = list()

l.append(sh.occ.addLine(p[1], p[0]))
l.append(sh.occ.addLine(p[0], p[2]))
l.append(sh.occ.addLine(p[2], p[3]))
l.append(sh.occ.addLine(p[3], p[1]))

l.append(sh.occ.addLine(p[4], p[5]))
l.append(sh.occ.addLine(p[4], p[6]))
l.append(sh.occ.addLine(p[6], p[7]))
l.append(sh.occ.addLine(p[5], p[7]))

l.append(sh.occ.addLine(p[4], p[0]))
l.append(sh.occ.addLine(p[5], p[1]))
l.append(sh.occ.addLine(p[2], p[6]))
l.append(sh.occ.addLine(p[3], p[7]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = list()
s = list()

k.append(sh.occ.addCurveLoop([l[0], l[1], l[2], l[3]]))
k.append(sh.occ.addCurveLoop([l[7], l[6], l[5], l[4]]))
k.append(sh.occ.addCurveLoop([l[5], l[10], l[1], l[8]]))
k.append(sh.occ.addCurveLoop([l[9], l[3], l[11], l[7]]))
k.append(sh.occ.addCurveLoop([l[8], l[4], l[9], l[0]]))
k.append(sh.occ.addCurveLoop([l[10], l[2], l[11], l[6]]))

for a in k: s.append(sh.occ.addPlaneSurface([a]))
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(l[1], N)
sh.mesh.setTransfiniteCurve(l[3], N)
sh.mesh.setTransfiniteCurve(l[5], N)
sh.mesh.setTransfiniteCurve(l[7], N)

sh.mesh.setTransfiniteCurve(l[0], M)
sh.mesh.setTransfiniteCurve(l[2], M)
sh.mesh.setTransfiniteCurve(l[4], M)
sh.mesh.setTransfiniteCurve(l[6], M)
sh.mesh.setTransfiniteCurve(l[8], M)
sh.mesh.setTransfiniteCurve(l[9], M)
sh.mesh.setTransfiniteCurve(l[10], M)
sh.mesh.setTransfiniteCurve(l[11], M)

for a in s: sh.mesh.setTransfiniteSurface(a)
for a in s: sh.mesh.setRecombine(2, a)

# Volumes List

h = sh.occ.addSurfaceLoop(s)
v = sh.occ.addVolume([h])

sh.occ.synchronize()
sh.mesh.setTransfiniteVolume(v)
sh.mesh.setRecombine(3, v)

# Physical Surface

sh.addPhysicalGroup(3, [v], name='Solid')
sh.addPhysicalGroup(2, s[5:6], name='FSInterface')
sh.addPhysicalGroup(2, s[0:4], name='Clamped')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(3)
gmsh.write(os.path.dirname(__file__) + '/geometry_S.msh')
gmsh.fltk.run()
gmsh.finalize()