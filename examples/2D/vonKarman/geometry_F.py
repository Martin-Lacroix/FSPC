import os, gmsh
import numpy as np
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

L = 1.5
H = 0.41
R = 0.05
CX = 0.2
CY = 0.2
BX = 0.6
BH = 0.01

# Characteristic size

d = 4e-3
LN = 376
N = 88
M = 6

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()
A = np.sqrt(np.square(R)-np.square(BH))

p.append(sh.occ.addPoint(0, 0, 0, d))
p.append(sh.occ.addPoint(L, 0, 0, d))
p.append(sh.occ.addPoint(L, H, 0, d))
p.append(sh.occ.addPoint(0, H, 0, d))

p.append(sh.occ.addPoint(CX, CY, 0, d))
p.append(sh.occ.addPoint(CX-R, CY, 0, d))

p.append(sh.occ.addPoint(BX, CY-BH, 0, d))
p.append(sh.occ.addPoint(BX, CY + BH, 0, d))
p.append(sh.occ.addPoint(CX + A, CY-BH, 0, d))
p.append(sh.occ.addPoint(CX + A, CY + BH, 0, d))

# Lines List

l = list()
h = list()
r = list()

l.append(sh.occ.addLine(p[0], p[1]))
l.append(sh.occ.addLine(p[1], p[2]))
l.append(sh.occ.addLine(p[2], p[3]))
l.append(sh.occ.addLine(p[3], p[0]))

h.append(sh.occ.addCircleArc(p[9], p[4], p[5]))
h.append(sh.occ.addCircleArc(p[5], p[4], p[8]))

r.append(sh.occ.addLine(p[8], p[6]))
r.append(sh.occ.addLine(p[6], p[7]))
r.append(sh.occ.addLine(p[7], p[9]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop(l)
u = sh.occ.addCurveLoop(h + r)
s = sh.occ.addPlaneSurface([k, -u])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(r[0], N)
sh.mesh.setTransfiniteCurve(r[1], M)
sh.mesh.setTransfiniteCurve(r[2], N)

# Physical Boundary

sh.addPhysicalGroup(2, [s], name='Fluid')
sh.addPhysicalGroup(1, r, name='FSInterface')
sh.addPhysicalGroup(1, l[1:2], name='Outlet')
sh.addPhysicalGroup(1, [l[0], l[2]] + h, name='Wall')
sh.addPhysicalGroup(1, l[3:4], name='Inlet')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(2)
gmsh.option.setNumber('Mesh.SaveParametric', 1)
gmsh.write(os.path.dirname(__file__) + '/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()