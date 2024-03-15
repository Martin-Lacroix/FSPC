import os, gmsh
import numpy as np
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

L1 = 0.3
L2 = 0.5
L3 = 0.8

R1 = 0.3
R2 = 0.25

Y = -0.01
B = 0.15
S = 0.04
W = 0.02

# Characteristic size

d = 0.02
E = 1e-3
N = 18
M = 9
P = 2

# |--------------------------------|
# |   Function to Make a Circle    |
# |--------------------------------|

def quad_circle(x,y):

    A = 0.6*R2
    p = list()

    p.append(sh.occ.addPoint(x, y, 0, d))
    p.append(sh.occ.addPoint(x, y-R2, 0, d))
    p.append(sh.occ.addPoint(x, y, R2, d))
    p.append(sh.occ.addPoint(x, y+R2, 0, d))
    p.append(sh.occ.addPoint(x, y, -R2, d))
    p.append(sh.occ.addPoint(x, y-A, 0, d))
    p.append(sh.occ.addPoint(x, y, A, d))
    p.append(sh.occ.addPoint(x, y+A, 0, d))
    p.append(sh.occ.addPoint(x, y, -A, d))

    # Lines list

    l = list()
    c = list()

    c.append(sh.occ.addCircleArc(p[1], p[0], p[2]))
    c.append(sh.occ.addCircleArc(p[2], p[0], p[3]))
    c.append(sh.occ.addCircleArc(p[3], p[0], p[4]))
    c.append(sh.occ.addCircleArc(p[4], p[0], p[1]))

    l.append(sh.occ.addLine(p[5], p[6]))
    l.append(sh.occ.addLine(p[6], p[7]))
    l.append(sh.occ.addLine(p[7], p[8]))
    l.append(sh.occ.addLine(p[8], p[5]))
    l.append(sh.occ.addLine(p[5], p[1]))
    l.append(sh.occ.addLine(p[6], p[2]))
    l.append(sh.occ.addLine(p[7], p[3]))
    l.append(sh.occ.addLine(p[8], p[4]))

    # Surfaces List

    k = list()
    s = list()

    k.append(sh.occ.addCurveLoop([l[0], l[1], l[2], l[3]]))
    k.append(sh.occ.addCurveLoop([l[4], c[0], l[5], l[0]]))
    k.append(sh.occ.addCurveLoop([l[5], c[1], l[6], l[1]]))
    k.append(sh.occ.addCurveLoop([l[6], c[2], l[7], l[2]]))
    k.append(sh.occ.addCurveLoop([l[7], c[3], l[4], l[3]]))

    for a in k: s.append(sh.occ.addPlaneSurface([a]))
    sh.occ.synchronize()

    # Transfinite mesh

    for a in c: sh.mesh.setTransfiniteCurve(a, N)
    for a in l[:4]: sh.mesh.setTransfiniteCurve(a, N)
    for a in l[4:]: sh.mesh.setTransfiniteCurve(a, M)
    for a in s: sh.mesh.setTransfiniteSurface(a)
    for a in s: sh.mesh.setRecombine(2, a)
    return s

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()
q = list()

p.append(sh.occ.addPoint(L1, -R1, 0, d))
p.append(sh.occ.addPoint(L1+L2+L3+S, -R1, 0, d))
p.append(sh.occ.addPoint(L1+L2+S/2, -B, 0, d))

p.append(sh.occ.addPoint(L1, S-R1, 0, d))
p.append(sh.occ.addPoint(L1+L2, S-R1, 0, d))
p.append(sh.occ.addPoint(L1+L2, -B, 0, d))
p.append(sh.occ.addPoint(L1+L2+S, -B, 0, d))
p.append(sh.occ.addPoint(L1+L2+S, S-R1, 0, d))
p.append(sh.occ.addPoint(L1+L2+L3+S, S-R1, 0, d))

# Lines list

l = list()
h = list()

l.append(sh.occ.addLine(p[0], p[1]))
l.append(sh.occ.addLine(p[1], p[8]))
l.append(sh.occ.addLine(p[8], p[7]))
l.append(sh.occ.addLine(p[7], p[6]))
l.append(sh.occ.addCircleArc(p[5], p[2], p[6]))
l.append(sh.occ.addLine(p[5], p[4]))
l.append(sh.occ.addLine(p[4], p[3]))
l.append(sh.occ.addLine(p[3], p[0]))

# |--------------------------------------|
# |   Surfaces and Volumes Definition    |
# |--------------------------------------|

tags = [(2,a) for a in quad_circle(L1+L2-E, Y+E)]
ext = sh.occ.extrude(tags, -W, 0, 0, [P], recombine=True)
ext = np.transpose(ext)
sh.occ.synchronize()

idx = np.argwhere(ext[0]==3).flatten()
s = sh.getBoundary(np.transpose(ext[:, idx]), 1, 0, 0)
s = np.transpose(s)[1]
w = ext[1, idx]

# Solid tool

k = sh.occ.addPlaneSurface([sh.occ.addCurveLoop(l)])
rev = sh.occ.revolve([(2,k)], 0, 0, 0, 1, 0, 0, 2*np.pi)[1:]
rev = np.transpose(rev)
sh.occ.synchronize()

v = rev[1, np.argwhere(rev[0]==3).flatten()]
x = rev[1, np.argwhere(rev[0]==2).flatten()]

# |-----------------------------------|
# |   Physical Volume and Boundary    |
# |-----------------------------------|

sh.addPhysicalGroup(3, v, name='Tool')
sh.addPhysicalGroup(3, w, name='Solid')
sh.addPhysicalGroup(2, s, name='FSInterface')
sh.addPhysicalGroup(2, x, name='Contact')

# Write the mesh

sh.mesh.generate(3)
gmsh.write(os.path.dirname(__file__)+'/geometry_S.msh')
gmsh.fltk.run()
gmsh.finalize()