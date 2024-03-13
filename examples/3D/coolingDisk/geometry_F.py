import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

RS = 0.0125
HS = 0.014
HF = 0.05
RF = 0.1

d = 3.7e-3

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(0, 0, 0, d))
p.append(sh.occ.addPoint(RF, 0, 0, d))
p.append(sh.occ.addPoint(-RF, 0, 0, d))
p.append(sh.occ.addPoint(0, RF, 0, d))
p.append(sh.occ.addPoint(0, -RF, 0, d))
p.append(sh.occ.addPoint(0, 0, HF, d))
p.append(sh.occ.addPoint(RF, 0, HF, d))
p.append(sh.occ.addPoint(-RF, 0, HF, d))
p.append(sh.occ.addPoint(0, RF, HF, d))
p.append(sh.occ.addPoint(0, -RF, HF, d))
p.append(sh.occ.addPoint(0, 0, HF + HS + RS, d))
p.append(sh.occ.addPoint(0, -RF, HF + HS + RS, d))
p.append(sh.occ.addPoint(RF, 0, HF + HS + RS, d))
p.append(sh.occ.addPoint(-RF, 0, HF + HS + RS, d))
p.append(sh.occ.addPoint(0, RF, HF + HS + RS, d))

# # Lines List

l = list()
c = list()

c.append(sh.occ.addCircleArc(p[2], p[0], p[4]))
c.append(sh.occ.addCircleArc(p[4], p[0], p[1]))
c.append(sh.occ.addCircleArc(p[1], p[0], p[3]))
c.append(sh.occ.addCircleArc(p[3], p[0], p[2]))
c.append(sh.occ.addCircleArc(p[7], p[5], p[9]))
c.append(sh.occ.addCircleArc(p[9], p[5], p[6]))
c.append(sh.occ.addCircleArc(p[6], p[5], p[8]))
c.append(sh.occ.addCircleArc(p[8], p[5], p[7]))
c.append(sh.occ.addCircleArc(p[14], p[10], p[13]))
c.append(sh.occ.addCircleArc(p[13], p[10], p[11]))
c.append(sh.occ.addCircleArc(p[11], p[10], p[12]))
c.append(sh.occ.addCircleArc(p[12], p[10], p[14]))

l.append(sh.occ.addLine(p[8], p[3]))
l.append(sh.occ.addLine(p[6], p[1]))
l.append(sh.occ.addLine(p[2], p[7]))
l.append(sh.occ.addLine(p[9], p[4]))
l.append(sh.occ.addLine(p[6], p[12]))
l.append(sh.occ.addLine(p[8], p[14]))
l.append(sh.occ.addLine(p[7], p[13]))
l.append(sh.occ.addLine(p[11], p[9]))

# |--------------------------------------|
# |   Surfaces and Volumes Definition    |
# |--------------------------------------|

k = list()
s = list()

k.append(sh.occ.addCurveLoop([c[4], c[5], c[6], c[7]]))
k.append(sh.occ.addCurveLoop([c[1], c[2], c[3], c[0]]))
k.append(sh.occ.addCurveLoop([l[1], c[2], l[0], c[6]]))
k.append(sh.occ.addCurveLoop([c[3], l[2], c[7], l[0]]))
k.append(sh.occ.addCurveLoop([c[0], l[3], c[4], l[2]]))
k.append(sh.occ.addCurveLoop([c[1], l[1], c[5], l[3]]))
k.append(sh.occ.addCurveLoop([l[6], c[8], l[5], c[7]]))
k.append(sh.occ.addCurveLoop([c[9], l[7], c[4], l[6]]))
k.append(sh.occ.addCurveLoop([c[5], l[4], c[10], l[7]]))
k.append(sh.occ.addCurveLoop([c[6], l[5], c[11], l[4]]))

for a in k: s.append(sh.occ.addBSplineFilling(a))
sh.occ.synchronize()

# Volumes List

h = sh.occ.addSurfaceLoop(s[:6])
u = sh.occ.addSphere(0, 0, HS + HF, RS)
v = sh.occ.addVolume([h])
sh.occ.synchronize()

g = sh.getBoundary([(3, u)], 0, 0, 0)[0][1]
p = sh.getBoundary([(3, u)], 0, 0, 1)
sh.occ.remove([(3, u)])
sh.mesh.setSize(p, d)
sh.occ.synchronize()

# Physical Surface

sh.addPhysicalGroup(3, [v], name='Fluid')
sh.addPhysicalGroup(2, [g], name='FSInterface')
sh.addPhysicalGroup(2, s[0:1], name='FreeSurface')
sh.addPhysicalGroup(2, s[1:], name='Wall')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(3)
gmsh.write(os.path.dirname(__file__) + '/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()