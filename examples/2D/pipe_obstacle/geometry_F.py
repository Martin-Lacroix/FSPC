import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# Mesh Parameters

L1 = 0.3
L2 = 0.5
L3 = 0.8

R1 = 0.26
R2 = 0.24

Y = -0.02
H = 0.05
L = 0.1
B = 0.15

R = 0.02
S = 0.04
W = 0.02

d = 0.005
E = 1e-3
N = 101
M = 5

# Points list

p = list()
q = list()
u = list()
v = list()

v.append(sh.occ.addPoint(L1+L2-E-W, Y-R2, 0, d))
v.append(sh.occ.addPoint(L1+L2-E, Y-R2, 0, d))
v.append(sh.occ.addPoint(L1+L2-E, Y+R2, 0, d))
v.append(sh.occ.addPoint(L1+L2-E-W, Y+R2, 0, d))

p.append(sh.occ.addPoint(0, -H, 0, d))
p.append(sh.occ.addPoint(L, -H, 0, d))
p.append(sh.occ.addPoint(L1-R, -H, 0, d))
p.append(sh.occ.addPoint(L1-R, -H-R, 0, d))
p.append(sh.occ.addPoint(L1, -H-R, 0, d))

p.append(sh.occ.addPoint(L1, -R1, 0, d))
p.append(sh.occ.addPoint(L1+L2, -R1, 0, d))
p.append(sh.occ.addPoint(L1+L2, -B, 0, d))
p.append(sh.occ.addPoint(L1+L2+S/2, -B, 0, d))
p.append(sh.occ.addPoint(L1+L2+S, -B, 0, d))

p.append(sh.occ.addPoint(L1+L2+S, -R1, 0, d))
p.append(sh.occ.addPoint(L1+L2+L3+S, -R1, 0, d))

q.append(sh.occ.addPoint(0, H, 0, d))
q.append(sh.occ.addPoint(L, H, 0, d))
q.append(sh.occ.addPoint(L1-R, H, 0, d))
q.append(sh.occ.addPoint(L1-R, H+R, 0, d))
q.append(sh.occ.addPoint(L1, H+R, 0, d))

q.append(sh.occ.addPoint(L1, R1, 0, d))
q.append(sh.occ.addPoint(L1+L2, R1, 0, d))
q.append(sh.occ.addPoint(L1+L2, B, 0, d))
q.append(sh.occ.addPoint(L1+L2+S/2, B, 0, d))
q.append(sh.occ.addPoint(L1+L2+S, B, 0, d))

q.append(sh.occ.addPoint(L1+L2+S, R1, 0, d))
q.append(sh.occ.addPoint(L1+L2+L3+S, R1, 0, d))

# Lines list

l = list()
h = list()
r = list()
b = list()

l.append(sh.occ.addLine(p[0], p[1]))
l.append(sh.occ.addLine(p[1], p[2]))
l.append(sh.occ.addCircleArc(p[2], p[3], p[4]))
l.append(sh.occ.addLine(p[4], p[5]))
l.append(sh.occ.addLine(p[5], p[6]))
l.append(sh.occ.addLine(p[6], p[7]))
l.append(sh.occ.addCircleArc(p[7], p[8], p[9]))
l.append(sh.occ.addLine(p[9], p[10]))
l.append(sh.occ.addLine(p[10], p[11]))

h.append(sh.occ.addLine(q[0], q[1]))
h.append(sh.occ.addLine(q[1], q[2]))
h.append(sh.occ.addCircleArc(q[2], q[3], q[4]))
h.append(sh.occ.addLine(q[4], q[5]))
h.append(sh.occ.addLine(q[5], q[6]))
h.append(sh.occ.addLine(q[6], q[7]))
h.append(sh.occ.addCircleArc(q[9], q[8], q[7]))
h.append(sh.occ.addLine(q[9], q[10]))
h.append(sh.occ.addLine(q[10], q[11]))

# Inlet and free surface

r.append(sh.occ.addLine(p[0], q[0]))
r.append(sh.occ.addLine(p[1], q[1]))

# Solid square

b.append(sh.occ.addLine(v[0], v[1]))
b.append(sh.occ.addLine(v[1], v[2]))
b.append(sh.occ.addLine(v[2], v[3]))
b.append(sh.occ.addLine(v[3], v[0]))

# Physical surface

k = sh.occ.addCurveLoop([l[0], r[0], h[0], r[1]])
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(b[0], M)
sh.mesh.setTransfiniteCurve(b[1], N)
sh.mesh.setTransfiniteCurve(b[2], M)
sh.mesh.setTransfiniteCurve(b[3], N)

# Physical boundary

sh.addPhysicalGroup(2, [s], name='Fluid')
sh.addPhysicalGroup(1, b, name='FSInterface')
sh.addPhysicalGroup(1, r[0:1], name='Inlet')
sh.addPhysicalGroup(1, l+h, name='Border')

# Write the mesh file

sh.mesh.generate(2)
gmsh.write(f'{os.path.dirname(__file__)}/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()