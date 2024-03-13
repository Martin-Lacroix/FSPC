import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

L1 = 0.3
L2 = 0.5
L3 = 0.8

H1 = 0.2
H2 = 0.1
H3 = 0.3

B = 0.13
S = 0.04

h = 0.5
w = 0.02

# Characteristic size

d = 0.005
eps = 1e-3
N = 101
M = 5

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(L1 + L2-eps, S + eps, 0, d))
p.append(sh.occ.addPoint(L1 + L2-eps, S + h + eps, 0, d))
p.append(sh.occ.addPoint(L1 + L2-w-eps, S + eps, 0, d))
p.append(sh.occ.addPoint(L1 + L2-w-eps, S + h + eps, 0, d))

p.append(sh.occ.addPoint(L1, 0, 0, d))
p.append(sh.occ.addPoint(L1 + L2 + L3 + S, 0, 0, d))
p.append(sh.occ.addPoint(L1 + L2 + L3 + S, H1 + H2 + H3, 0, d))
p.append(sh.occ.addPoint(L1, H1 + H2 + H3, 0, d))

p.append(sh.occ.addPoint(L1 + L2 + S/2, S + B, 0, d))
p.append(sh.occ.addPoint(L1 + L2 + S/2, H1 + H2 + H3-S-B, 0, d))

p.append(sh.occ.addPoint(L1, S, 0, d))
p.append(sh.occ.addPoint(L1 + L2, S, 0, d))
p.append(sh.occ.addPoint(L1 + L2, S + B, 0, d))
p.append(sh.occ.addPoint(L1 + L2 + S, S + B, 0, d))
p.append(sh.occ.addPoint(L1 + L2 + S, S, 0, d))
p.append(sh.occ.addPoint(L1 + L2 + L3 + S, S, 0, d))

p.append(sh.occ.addPoint(L1, H1 + H2 + H3-S, 0, d))
p.append(sh.occ.addPoint(L1 + L2, H1 + H2 + H3-S, 0, d))
p.append(sh.occ.addPoint(L1 + L2, H1 + H2 + H3-S-B, 0, d))
p.append(sh.occ.addPoint(L1 + L2 + S, H1 + H2 + H3-S-B, 0, d))
p.append(sh.occ.addPoint(L1 + L2 + S, H1 + H2 + H3-S, 0, d))
p.append(sh.occ.addPoint(L1 + L2 + L3 + S, H1 + H2 + H3-S, 0, d))

# Lines List

l = list()
r = list()
h = list()

l.append(sh.occ.addLine(p[4], p[5]))
l.append(sh.occ.addLine(p[5], p[15]))
l.append(sh.occ.addLine(p[15], p[14]))
l.append(sh.occ.addLine(p[14], p[13]))
l.append(sh.occ.addCircleArc(p[12], p[8], p[13]))
l.append(sh.occ.addLine(p[12], p[11]))
l.append(sh.occ.addLine(p[11], p[10]))
l.append(sh.occ.addLine(p[10], p[4]))

r.append(sh.occ.addLine(p[7], p[16]))
r.append(sh.occ.addLine(p[16], p[17]))
r.append(sh.occ.addLine(p[17], p[18]))
r.append(sh.occ.addCircleArc(p[19], p[9], p[18]))
r.append(sh.occ.addLine(p[19], p[20]))
r.append(sh.occ.addLine(p[20], p[21]))
r.append(sh.occ.addLine(p[21], p[6]))
r.append(sh.occ.addLine(p[6], p[7]))

# Solid square

h.append(sh.occ.addLine(p[2], p[0]))
h.append(sh.occ.addLine(p[0], p[1]))
h.append(sh.occ.addLine(p[1], p[3]))
h.append(sh.occ.addLine(p[3], p[2]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = list()
s = list()

k.append(sh.occ.addCurveLoop(h))
k.append(sh.occ.addCurveLoop(l))
k.append(sh.occ.addCurveLoop(r))
for a in k: s.append(sh.occ.addPlaneSurface([a]))
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(h[0], M)
sh.mesh.setTransfiniteCurve(h[1], N)
sh.mesh.setTransfiniteCurve(h[2], M)
sh.mesh.setTransfiniteCurve(h[3], N)

sh.mesh.setTransfiniteSurface(s[0])
sh.mesh.setRecombine(2, s[0])

# Boundaries

sh.addPhysicalGroup(2, s[1:3], name='Tool')
sh.addPhysicalGroup(2, s[0:1], name='Solid')
sh.addPhysicalGroup(1, h, name='FSInterface')
sh.addPhysicalGroup(1, l + r, name='Contact')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__) + '/geometry_S.msh')
gmsh.fltk.run()
gmsh.finalize()