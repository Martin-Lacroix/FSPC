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

F = 0.1
B = 0.13
R = 0.02
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

p.append(sh.occ.addPoint(0, H1, 0, d))
p.append(sh.occ.addPoint(L1-R, H1, 0, d))
p.append(sh.occ.addPoint(L1-R, H1-R, 0, d))
p.append(sh.occ.addPoint(L1, H1-R, 0, d))

p.append(sh.occ.addPoint(L1, H1 + H2 + R, 0, d))
p.append(sh.occ.addPoint(L1-R, H1 + H2 + R, 0, d))
p.append(sh.occ.addPoint(L1-R, H1 + H2, 0, d))
p.append(sh.occ.addPoint(0, H1 + H2, 0, d))

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

p.append(sh.occ.addPoint(F, H1, 0, d))
p.append(sh.occ.addPoint(F, H1 + H2, 0, d))
p.append(sh.occ.addPoint(L1 + L2 + S/2, S + B, 0, d))
p.append(sh.occ.addPoint(L1 + L2 + S/2, H1 + H2 + H3-S-B, 0, d))

p.append(sh.occ.addPoint(L1 + L2-eps, S + eps, 0, d))
p.append(sh.occ.addPoint(L1 + L2-eps, S + h + eps, 0, d))
p.append(sh.occ.addPoint(L1 + L2-w-eps, S + eps, 0, d))
p.append(sh.occ.addPoint(L1 + L2-w-eps, S + h + eps, 0, d))

# Lines List

l = list()
h = list()
r = list()

l.append(sh.occ.addLine(p[0], p[20]))
l.append(sh.occ.addLine(p[21], p[7]))

l.append(sh.occ.addLine(p[13], p[12]))
l.append(sh.occ.addLine(p[12], p[11]))
l.append(sh.occ.addCircleArc(p[10], p[22], p[11]))
l.append(sh.occ.addLine(p[10], p[9]))
l.append(sh.occ.addLine(p[9], p[8]))

l.append(sh.occ.addLine(p[14], p[15]))
l.append(sh.occ.addLine(p[15], p[16]))
l.append(sh.occ.addCircleArc(p[17], p[23], p[16]))
l.append(sh.occ.addLine(p[17], p[18]))
l.append(sh.occ.addLine(p[18], p[19]))

l.append(sh.occ.addLine(p[20], p[1]))
l.append(sh.occ.addCircleArc(p[1], p[2], p[3]))
l.append(sh.occ.addLine(p[3], p[8]))
l.append(sh.occ.addLine(p[21], p[6]))
l.append(sh.occ.addCircleArc(p[6], p[5], p[4]))
l.append(sh.occ.addLine(p[4], p[14]))

# Inlet and free surface

r.append(sh.occ.addLine(p[7], p[0]))
r.append(sh.occ.addLine(p[20], p[21]))

# Solid square

h.append(sh.occ.addLine(p[26], p[24]))
h.append(sh.occ.addLine(p[24], p[25]))
h.append(sh.occ.addLine(p[25], p[27]))
h.append(sh.occ.addLine(p[27], p[26]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop([l[0], r[0], l[1], r[1]])
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(h[0], M)
sh.mesh.setTransfiniteCurve(h[1], N)
sh.mesh.setTransfiniteCurve(h[2], M)
sh.mesh.setTransfiniteCurve(h[3], N)

# Physical Boundary

sh.addPhysicalGroup(2, [s], name='Fluid')
sh.addPhysicalGroup(1, h, name='FSInterface')
sh.addPhysicalGroup(1, r[1:2], name='FreeSurface')
sh.addPhysicalGroup(1, r[0:1], name='Inlet')
sh.addPhysicalGroup(1, l, name='Border')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__) + '/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()