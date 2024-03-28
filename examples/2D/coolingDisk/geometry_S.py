import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

L = 0.9
HF = 0.25
HS = 0.03
R = 0.025

# Characteristic size

N = 9
M = 5

# |--------------------------------|
# |   Function to Make a Circle    |
# |--------------------------------|

def quad_circle(x):

    A = 0.6*R
    p = list()

    p.append(sh.occ.addPoint(x, HF+HS, 0))
    p.append(sh.occ.addPoint(x, HF+HS-R, 0))
    p.append(sh.occ.addPoint(x+R, HF+HS, 0))
    p.append(sh.occ.addPoint(x, HF+HS+R, 0))
    p.append(sh.occ.addPoint(x-R, HF+HS, 0))
    p.append(sh.occ.addPoint(x, HF+HS-A, 0))
    p.append(sh.occ.addPoint(x+A, HF+HS, 0))
    p.append(sh.occ.addPoint(x, HF+HS+A, 0))
    p.append(sh.occ.addPoint(x-A, HF+HS, 0))

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
    return s, c

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

s, l = quad_circle(0.2)
u, h = quad_circle(0.45)
v, c = quad_circle(0.7)

sh.addPhysicalGroup(2, s, name='S1')
sh.addPhysicalGroup(2, u, name='S2')
sh.addPhysicalGroup(2, v, name='S3')
sh.addPhysicalGroup(2, s+u+v, name='Solid')
sh.addPhysicalGroup(1, l+h+c, name='FSInterface')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__)+'/geometry_S.msh')
gmsh.fltk.run()
gmsh.finalize()