import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

R = 0.25
L = 0.15+R
H = -0.125

L1 = 0.25+R
L2 = 0.6-2*R

D1 = 3.75-10*R
D2 = 1.25

HB = 0.75+H+5*R
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
q = list()
r = list()

p.append(sh.occ.addPoint(-(L+L1+L2), H-5*R, 0, d))
p.append(sh.occ.addPoint(-(L+L1+L2), H+5*R, 0, d))

p.append(sh.occ.addPoint(-L, H+5*R, 0, d))
p.append(sh.occ.addPoint(-L, H+4*R, 0, d))
p.append(sh.occ.addPoint(-L, H+3*R, 0, d))

p.append(sh.occ.addPoint(-(L+L2), H+3*R, 0, d))
p.append(sh.occ.addPoint(-(L+L2), H+2*R, 0, d))
p.append(sh.occ.addPoint(-(L+L2), H+R, 0, d))

p.append(sh.occ.addPoint(-L, H+R, 0, d))
p.append(sh.occ.addPoint(-L, H, 0, d))
p.append(sh.occ.addPoint(-L, H-R, 0, d))

p.append(sh.occ.addPoint(-(L+L2), H-R, 0, d))
p.append(sh.occ.addPoint(-(L+L2), H-2*R, 0, d))
p.append(sh.occ.addPoint(-(L+L2), H-3*R, 0, d))

p.append(sh.occ.addPoint(-L, H-3*R, 0, d))
p.append(sh.occ.addPoint(-L, H-4*R, 0, d))
p.append(sh.occ.addPoint(-L, H-5*R, 0, d))

q.append(sh.occ.addPoint(L+L1+L2, -H-5*R, 0, d))
q.append(sh.occ.addPoint(L+L1+L2, -H+5*R, 0, d))

q.append(sh.occ.addPoint(L, -H+5*R, 0, d))
q.append(sh.occ.addPoint(L, -H+4*R, 0, d))
q.append(sh.occ.addPoint(L, -H+3*R, 0, d))

q.append(sh.occ.addPoint(L+L2, -H+3*R, 0, d))
q.append(sh.occ.addPoint(L+L2, -H+2*R, 0, d))
q.append(sh.occ.addPoint(L+L2, -H+R, 0, d))

q.append(sh.occ.addPoint(L, -H+R, 0, d))
q.append(sh.occ.addPoint(L, -H, 0, d))
q.append(sh.occ.addPoint(L, -H-R, 0, d))

q.append(sh.occ.addPoint(L+L2, -H-R, 0, d))
q.append(sh.occ.addPoint(L+L2, -H-2*R, 0, d))
q.append(sh.occ.addPoint(L+L2, -H-3*R, 0, d))

q.append(sh.occ.addPoint(L, -H-3*R, 0, d))
q.append(sh.occ.addPoint(L, -H-4*R, 0, d))
q.append(sh.occ.addPoint(L, -H-5*R, 0, d))

r.append(sh.occ.addPoint(-RB, HB, 0, d))
r.append(sh.occ.addPoint(0, HB, 0, d))
r.append(sh.occ.addPoint(RB, HB, 0, d))

# Lines list

l = list()
h = list()
c = list()

l.append(sh.occ.addLine(p[1], p[0]))
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

h.append(sh.occ.addLine(q[1], q[0]))
h.append(sh.occ.addLine(q[0], q[16]))
h.append(sh.occ.addCircleArc(q[16], q[15], q[14]))
h.append(sh.occ.addLine(q[14], q[13]))
h.append(sh.occ.addCircleArc(q[11], q[12], q[13]))
h.append(sh.occ.addLine(q[11], q[10]))
h.append(sh.occ.addCircleArc(q[10], q[9], q[8]))
h.append(sh.occ.addLine(q[8], q[7]))
h.append(sh.occ.addCircleArc(q[5], q[6], q[7]))
h.append(sh.occ.addLine(q[5], q[4]))
h.append(sh.occ.addCircleArc(q[4], q[3], q[2]))
h.append(sh.occ.addLine(q[2], q[1]))

c.append(sh.occ.addCircleArc(r[2], r[1], r[0]))
c.append(sh.occ.addCircleArc(r[0], r[1], r[2]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

x = sh.occ.addPlaneSurface([sh.occ.addCurveLoop(l)])
y = sh.occ.addPlaneSurface([sh.occ.addCurveLoop(h)])
z = sh.occ.addPlaneSurface([sh.occ.addCurveLoop(c)])

sh.occ.synchronize()
sh.mesh.setReverse(2, y)
sh.mesh.setReverse(2, z)

# Transfinite mesh

sh.mesh.setTransfiniteCurve(c[0], N)
sh.mesh.setTransfiniteCurve(c[1], N)

for i in (2,4,6,8,10):

    sh.mesh.setTransfiniteCurve(l[i], M)
    sh.mesh.setTransfiniteCurve(h[i], M)

for i in (3,5,7,9):

    sh.mesh.setTransfiniteCurve(l[i], P)
    sh.mesh.setTransfiniteCurve(h[i], P)

for i in (1,11):

    sh.mesh.setTransfiniteCurve(l[i], Q)
    sh.mesh.setTransfiniteCurve(h[i], Q)

# Physical boundary

sh.addPhysicalGroup(2, [z], name='Disk')
sh.addPhysicalGroup(2, [x, y], name='Wall')
sh.addPhysicalGroup(2, [x, y, z], name='Solid')

sh.addPhysicalGroup(1, c, name='Circle')
sh.addPhysicalGroup(1, l+h, name='Side')
sh.addPhysicalGroup(1, l[0:1]+h[0:1], name='Clamped')
sh.addPhysicalGroup(1, l[1:]+h[1:]+c, name='FSInterface')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

gmsh.option.setNumber('Mesh.RecombineAll', 1)
gmsh.option.setNumber('Mesh.Algorithm', 6)
sh.mesh.generate(2)

gmsh.write(os.path.dirname(__file__)+'/geometry_S.msh')
gmsh.fltk.run()
gmsh.finalize()