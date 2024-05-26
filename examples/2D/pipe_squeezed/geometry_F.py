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

p.append(sh.occ.addPoint(L+L1+L2, -H-5*R, 0, d))
p.append(sh.occ.addPoint(L+L1+L2, -H+5*R, 0, d))

p.append(sh.occ.addPoint(L, -H+5*R, 0, d))
p.append(sh.occ.addPoint(L, -H+4*R, 0, d))
p.append(sh.occ.addPoint(L, -H+3*R, 0, d))

p.append(sh.occ.addPoint(L+L2, -H+3*R, 0, d))
p.append(sh.occ.addPoint(L+L2, -H+2*R, 0, d))
p.append(sh.occ.addPoint(L+L2, -H+R, 0, d))

p.append(sh.occ.addPoint(L, -H+R, 0, d))
p.append(sh.occ.addPoint(L, -H, 0, d))
p.append(sh.occ.addPoint(L, -H-R, 0, d))

p.append(sh.occ.addPoint(L+L2, -H-R, 0, d))
p.append(sh.occ.addPoint(L+L2, -H-2*R, 0, d))
p.append(sh.occ.addPoint(L+L2, -H-3*R, 0, d))

p.append(sh.occ.addPoint(L, -H-3*R, 0, d))
p.append(sh.occ.addPoint(L, -H-4*R, 0, d))
p.append(sh.occ.addPoint(L, -H-5*R, 0, d))

p.append(sh.occ.addPoint(-RB, HB, 0, d))
p.append(sh.occ.addPoint(0, HB, 0, d))
p.append(sh.occ.addPoint(RB, HB, 0, d))

p.append(sh.occ.addPoint(-(L+L1+L2), H-(5*R+D1), 0, d))
p.append(sh.occ.addPoint(-(L+L1+L2), H+5*R+D2, 0, d))
p.append(sh.occ.addPoint(L+L1+L2, H+5*R+D2, 0, d))
p.append(sh.occ.addPoint(L+L1+L2, H-(5*R+D1), 0, d))

# Lines list

l = list()
r = list()
h = list()
q = list()
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

r.append(sh.occ.addLine(p[18], p[19]))
r.append(sh.occ.addCircleArc(p[21], p[20], p[19]))
r.append(sh.occ.addLine(p[21], p[22]))
r.append(sh.occ.addCircleArc(p[22], p[23], p[24]))
r.append(sh.occ.addLine(p[24], p[25]))
r.append(sh.occ.addCircleArc(p[27], p[26], p[25]))
r.append(sh.occ.addLine(p[27], p[28]))
r.append(sh.occ.addCircleArc(p[28], p[29], p[30]))
r.append(sh.occ.addLine(p[30], p[31]))
r.append(sh.occ.addCircleArc(p[33], p[32], p[31]))
r.append(sh.occ.addLine(p[33], p[17]))

h.append(sh.occ.addLine(p[1], p[38]))
h.append(sh.occ.addLine(p[38], p[39]))
h.append(sh.occ.addLine(p[39], p[18]))

q.append(sh.occ.addLine(p[17], p[40]))
q.append(sh.occ.addLine(p[40], p[37]))
q.append(sh.occ.addLine(p[37], p[0]))

c.append(sh.occ.addCircleArc(p[34], p[35], p[36]))
c.append(sh.occ.addCircleArc(p[36], p[35], p[34]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = list()

k.append(sh.occ.addCurveLoop(c))
k.append(sh.occ.addCurveLoop(l+h+r+q))
s = sh.occ.addPlaneSurface([k[1], -k[0]])
sh.occ.synchronize()

# Transfinite mesh

sh.mesh.setTransfiniteCurve(c[0], N)
sh.mesh.setTransfiniteCurve(c[1], N)

for i in (1,3,5,7,9):

    sh.mesh.setTransfiniteCurve(l[i], M)
    sh.mesh.setTransfiniteCurve(r[i], M)

for i in (2,4,6,8):

    sh.mesh.setTransfiniteCurve(l[i], P)
    sh.mesh.setTransfiniteCurve(r[i], P)

for i in (0,10):

    sh.mesh.setTransfiniteCurve(l[i], Q)
    sh.mesh.setTransfiniteCurve(r[i], Q)

# Physical boundary

sh.addPhysicalGroup(2, [s], name='Fluid')
sh.addPhysicalGroup(1, q[1:2], name='FreeSurface')
sh.addPhysicalGroup(1, h[0:1]+h[2:3]+q[0:1]+q[2:3], name='Wall')
sh.addPhysicalGroup(1, l+r+c, name='FSInterface')
sh.addPhysicalGroup(1, h[1:2], name='Inlet')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(2)
gmsh.model.mesh.reverse()
gmsh.write(os.path.dirname(__file__)+'/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()