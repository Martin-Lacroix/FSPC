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

H1 = 0.2
H2 = 0.1
H3 = 0.3

B = 0.13
S = 0.04
C = 0.4

R = 0.25
W = 0.02

# Characteristic size

d = 0.02
E = 1e-3
N = 101
M = 5

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()
q = list()

p.append(sh.occ.addPoint(L1, 0, 0, d))
p.append(sh.occ.addPoint(L1+L2+L3+S, 0, 0, d))
p.append(sh.occ.addPoint(L1+L2+S/2, S+B, 0, d))

p.append(sh.occ.addPoint(L1, S, 0, d))
p.append(sh.occ.addPoint(L1+L2, S, 0, d))
p.append(sh.occ.addPoint(L1+L2, S+B, 0, d))
p.append(sh.occ.addPoint(L1+L2+S, S+B, 0, d))
p.append(sh.occ.addPoint(L1+L2+S, S, 0, d))
p.append(sh.occ.addPoint(L1+L2+L3+S, S, 0, d))

q.append(sh.occ.addPoint(L1+L2-E, S+E, 0, d))
q.append(sh.occ.addPoint(L1+L2-E, S+R+E, 0, d))
q.append(sh.occ.addPoint(L1+L2-W-E, S+E, 0, d))
q.append(sh.occ.addPoint(L1+L2-W-E, S+R+E, 0, d))

# Lines List

l = list()

l.append(sh.occ.addLine(p[0], p[1]))
l.append(sh.occ.addLine(p[1], p[8]))
l.append(sh.occ.addLine(p[8], p[7]))
l.append(sh.occ.addLine(p[7], p[6]))
l.append(sh.occ.addCircleArc(p[5], p[2], p[6]))
l.append(sh.occ.addLine(p[5], p[4]))
l.append(sh.occ.addLine(p[4], p[3]))
l.append(sh.occ.addLine(p[3], p[0]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

s = sh.occ.addPlaneSurface([sh.occ.addCurveLoop(l)])

# rev = sh.occ.revolve([(2,s)], 0, C, 0 , 1 , 0, 0, 2*np.pi)
sh.occ.synchronize()

# print(rev)

# Boundaries

# sh.addPhysicalGroup(2, s[1:3], name='Tool')
# sh.addPhysicalGroup(2, s[0:1], name='Solid')
# sh.addPhysicalGroup(1, l, name='Contact')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(3)
gmsh.write(os.path.dirname(__file__)+'/geometry_S.msh')
gmsh.fltk.run()
gmsh.finalize()