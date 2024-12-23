import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# Mesh Parameters

L = 0.2
W = 0.2
HS = 0.04

M = 41
N = 5

# Points list

p = list()

p.append(sh.occ.addPoint(-L, -W, 0))
p.append(sh.occ.addPoint(L, -W, 0))
p.append(sh.occ.addPoint(-L, -W, HS))
p.append(sh.occ.addPoint(L, -W, HS))

p.append(sh.occ.addPoint(-L, W, 0))
p.append(sh.occ.addPoint(L, W, 0))
p.append(sh.occ.addPoint(-L, W, HS))
p.append(sh.occ.addPoint(L, W, HS))

# Lines list

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

# Physical surface

k = list()
s = list()

k.append(sh.occ.addCurveLoop([l[3], l[2], l[1], l[0]]))
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

# Volumes list

h = sh.occ.addSurfaceLoop(s)
v = sh.occ.addVolume([h])

sh.occ.synchronize()
sh.mesh.setTransfiniteVolume(v)
sh.mesh.setRecombine(3, v)

# Physical surface

sh.addPhysicalGroup(3, [v], name='Solid')
sh.addPhysicalGroup(2, s[5:6], name='FSI')
sh.addPhysicalGroup(2, s[0:4], name='Clamped')

# Write the mesh file

sh.mesh.generate(3)
gmsh.model.mesh.reverse()
gmsh.write(f'{os.path.dirname(__file__)}/geometry_S.msh')
gmsh.fltk.run()
gmsh.finalize()