import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

R = 0.25
L = 0.15 + R
H = -0.125

L1 = 0.25 + R
L2 = 0.6-2*R

D1 = 3.75-10*R
D2 = 1.25

HB = 0.75 + H + 5*R
RB = 0.375

# Characteristic size

d = 0.04
N = 30
M = 25
P = 4
Q = 15

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(-(L + L1 + L2), H-5*R, 0, d))
p.append(sh.occ.addPoint(-(L + L1 + L2), H + 5*R, 0, d))

p.append(sh.occ.addPoint(-L, H + 5*R, 0, d))
p.append(sh.occ.addPoint(-L, H + 4*R, 0, d))
p.append(sh.occ.addPoint(-L, H + 3*R, 0, d))

p.append(sh.occ.addPoint(-(L + L2), H + 3*R, 0, d))
p.append(sh.occ.addPoint(-(L + L2), H + 2*R, 0, d))
p.append(sh.occ.addPoint(-(L + L2), H + R, 0, d))

p.append(sh.occ.addPoint(-L, H + R, 0, d))
p.append(sh.occ.addPoint(-L, H, 0, d))
p.append(sh.occ.addPoint(-L, H-R, 0, d))

p.append(sh.occ.addPoint(-(L + L2), H-R, 0, d))
p.append(sh.occ.addPoint(-(L + L2), H-2*R, 0, d))
p.append(sh.occ.addPoint(-(L + L2), H-3*R, 0, d))

p.append(sh.occ.addPoint(-L, H-3*R, 0, d))
p.append(sh.occ.addPoint(-L, H-4*R, 0, d))
p.append(sh.occ.addPoint(-L, H-5*R, 0, d))

p.append(sh.occ.addPoint(L + L1 + L2, -H-5*R, 0, d))
p.append(sh.occ.addPoint(L + L1 + L2, -H + 5*R, 0, d))

p.append(sh.occ.addPoint(L, -H + 5*R, 0, d))
p.append(sh.occ.addPoint(L, -H + 4*R, 0, d))
p.append(sh.occ.addPoint(L, -H + 3*R, 0, d))

p.append(sh.occ.addPoint(L + L2, -H + 3*R, 0, d))
p.append(sh.occ.addPoint(L + L2, -H + 2*R, 0, d))
p.append(sh.occ.addPoint(L + L2, -H + R, 0, d))

p.append(sh.occ.addPoint(L, -H + R, 0, d))
p.append(sh.occ.addPoint(L, -H, 0, d))
p.append(sh.occ.addPoint(L, -H-R, 0, d))

p.append(sh.occ.addPoint(L + L2, -H-R, 0, d))
p.append(sh.occ.addPoint(L + L2, -H-2*R, 0, d))
p.append(sh.occ.addPoint(L + L2, -H-3*R, 0, d))

p.append(sh.occ.addPoint(L, -H-3*R, 0, d))
p.append(sh.occ.addPoint(L, -H-4*R, 0, d))
p.append(sh.occ.addPoint(L, -H-5*R, 0, d))

p.append(sh.occ.addPoint(-RB, HB, 0, d))
p.append(sh.occ.addPoint(0, HB, 0, d))
p.append(sh.occ.addPoint(RB, HB, 0, d))

# Lines List

l = list()
h = list()
c = list()

l.append(sh.occ.addLine(p[0], p[16]))
l.append(sh.occ.addCircleArc(p[14], p[15], p[16]))
l.append(sh.occ.addLine(p[14], p[13]))
l.append(sh.occ.addCircleArc(p[13], p[12], p[11]))
l.append(sh.occ.addLine(p[11], p[10]))
l.append(sh.occ.addCircleArc(p[8], p[9], p[10]))
l.append(sh.occ.addLine(p[8], p[7]))
l.append(sh.occ.addCircleArc(p[7], p[6], p[5]))
l.append(sh.occ.addLine(p[5], p[4]))
l.append(sh.occ.addCircleArc(p[2], p[3], p[4]))
l.append(sh.occ.addLine(p[2], p[1]))
l.append(sh.occ.addLine(p[1], p[0]))

h.append(sh.occ.addLine(p[17], p[18]))
h.append(sh.occ.addLine(p[18], p[19]))
h.append(sh.occ.addCircleArc(p[21], p[20], p[19]))
h.append(sh.occ.addLine(p[21], p[22]))
h.append(sh.occ.addCircleArc(p[22], p[23], p[24]))
h.append(sh.occ.addLine(p[24], p[25]))
h.append(sh.occ.addCircleArc(p[27], p[26], p[25]))
h.append(sh.occ.addLine(p[27], p[28]))
h.append(sh.occ.addCircleArc(p[28], p[29], p[30]))
h.append(sh.occ.addLine(p[30], p[31]))
h.append(sh.occ.addCircleArc(p[33], p[32], p[31]))
h.append(sh.occ.addLine(p[33], p[17]))

c.append(sh.occ.addCircleArc(p[36], p[35], p[34]))
c.append(sh.occ.addCircleArc(p[34], p[35], p[36]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = list()
s = list()

k.append(sh.occ.addCurveLoop(l))
k.append(sh.occ.addCurveLoop(h))
k.append(sh.occ.addCurveLoop(c))

for a in k: s.append(sh.occ.addPlaneSurface([a]))
sh.occ.synchronize()

sh.mesh.setAlgorithm(2, s[0], 8)
sh.mesh.setAlgorithm(2, s[1], 8)
sh.mesh.setReverse(2, s[2])
sh.occ.synchronize()

# Transfinite Mesh

sh.mesh.setTransfiniteCurve(c[0], N)
sh.mesh.setTransfiniteCurve(c[1], N)

sh.mesh.setTransfiniteCurve(l[1], M)
sh.mesh.setTransfiniteCurve(l[3], M)
sh.mesh.setTransfiniteCurve(l[5], M)
sh.mesh.setTransfiniteCurve(l[7], M)
sh.mesh.setTransfiniteCurve(l[9], M)

sh.mesh.setTransfiniteCurve(h[2], M)
sh.mesh.setTransfiniteCurve(h[4], M)
sh.mesh.setTransfiniteCurve(h[6], M)
sh.mesh.setTransfiniteCurve(h[8], M)
sh.mesh.setTransfiniteCurve(h[10], M)

sh.mesh.setTransfiniteCurve(l[2], P)
sh.mesh.setTransfiniteCurve(l[4], P)
sh.mesh.setTransfiniteCurve(l[6], P)
sh.mesh.setTransfiniteCurve(l[8], P)

sh.mesh.setTransfiniteCurve(h[3], P)
sh.mesh.setTransfiniteCurve(h[5], P)
sh.mesh.setTransfiniteCurve(h[7], P)
sh.mesh.setTransfiniteCurve(h[9], P)

sh.mesh.setTransfiniteCurve(l[0], Q)
sh.mesh.setTransfiniteCurve(l[10], Q)

sh.mesh.setTransfiniteCurve(h[1], Q)
sh.mesh.setTransfiniteCurve(h[11], Q)

# Boundaries

sh.addPhysicalGroup(2, s[2:3], name='Disk')
sh.addPhysicalGroup(2, s[0:2], name='Peigne')
sh.addPhysicalGroup(1, l[:11] + h[1:], name='PeigneSide')
sh.addPhysicalGroup(1, l[:11] + h[1:] + c, name='FSInterface')
sh.addPhysicalGroup(1, [l[11], h[0]], name='Clamped')
sh.addPhysicalGroup(1, c, name='DiskSide')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

gmsh.option.setNumber('Mesh.RecombineAll', 1)
gmsh.option.setNumber('Mesh.Algorithm', 6)
sh.mesh.generate(2)

gmsh.write(os.path.dirname(__file__) + '/geometry_S.msh')
gmsh.fltk.run()
gmsh.finalize()