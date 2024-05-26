import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

L = 1
W = 1
HF = 0.2
HS = 0.02

# Characteristic size

M = 21
N = 6

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(L, 0, HS))
p.append(sh.occ.addPoint(0, 0, HS))
p.append(sh.occ.addPoint(L, 0, HS+HF))
p.append(sh.occ.addPoint(0, 0, HS+HF))

p.append(sh.occ.addPoint(L, W, HS))
p.append(sh.occ.addPoint(0, W, HS))
p.append(sh.occ.addPoint(L, W, HS+HF))
p.append(sh.occ.addPoint(0, W, HS+HF))

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

# |--------------------------------------|
# |   Surfaces and Volumes Definition    |
# |--------------------------------------|

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

# Volumes list

h = sh.occ.addSurfaceLoop(s)
v = sh.occ.addVolume([h])
sh.occ.synchronize()

# Physical surface

sh.addPhysicalGroup(3, [v], name='Fluid')
sh.addPhysicalGroup(2, s[0:4], name='Wall')
sh.addPhysicalGroup(2, s[4:5], name='FSInterface')
sh.addPhysicalGroup(2, s[5:6], name='FreeSurface')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(3)
gmsh.write(os.path.dirname(__file__)+'/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()