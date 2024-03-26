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
H = 0.05
L = 0.1
B = 0.2

R = 0.02
S = 0.04
W = 0.02

# Characteristic size

d = 0.01
E = 1e-3

# |--------------------------------------|
# |   Surfaces and Volumes Definition    |
# |--------------------------------------|

v = sh.occ.addCylinder(L1+L2-E, Y, 0, -W, 0, 0, R2)
sh.occ.synchronize()

k = sh.getBoundary([(3, v)], 0, 0, 0)
q = sh.getBoundary([(3, v)], 0, 0, 1)
sh.occ.remove([(3, v)])
sh.mesh.setSize(q, d)
sh.occ.synchronize()

k = np.transpose(k)[1]

# Inlet and free surface

x = sh.occ.addCylinder(0, 0, 0, L, 0, 0, H)
sh.occ.rotate([(3, x)], 0, 0, 0, 1, 0, 0, np.pi/2)
sh.occ.synchronize()

y = sh.getBoundary([(3, x)], 0, 0, 0)
g = sh.getBoundary([(3, x)], 0, 0, 1)
sh.mesh.setSize(g, d)

y = np.transpose(y)[1]
g = np.transpose(g)[1]

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()
L = L1+L2+L3+S

p.append(sh.occ.addPoint(L1-R, -H, 0, d))
p.append(sh.occ.addPoint(L1-R, -H-R, 0, d))
p.append(sh.occ.addPoint(L1, -H-R, 0, d))

p.append(sh.occ.addPoint(L1, S-R1, 0, d))
p.append(sh.occ.addPoint(L1+L2, S-R1, 0, d))
p.append(sh.occ.addPoint(L1+L2, -B, 0, d))
p.append(sh.occ.addPoint(L1+L2+S/2, -B, 0, d))
p.append(sh.occ.addPoint(L1+L2+S, -B, 0, d))

p.append(sh.occ.addPoint(L1+L2+S, S-R1, 0, d))
p.append(sh.occ.addPoint(L, S-R1, 0, d))

# Lines list

l = list()

l.append(sh.occ.addLine(g[0], p[0]))
l.append(sh.occ.addCircleArc(p[0], p[1], p[2]))
l.append(sh.occ.addLine(p[2], p[3]))
l.append(sh.occ.addLine(p[3], p[4]))
l.append(sh.occ.addLine(p[4], p[5]))
l.append(sh.occ.addCircleArc(p[5], p[6], p[7]))
l.append(sh.occ.addLine(p[7], p[8]))
l.append(sh.occ.addLine(p[8], p[9]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

tags = [(1,a) for a in l]
rev = sh.occ.revolve(tags, 0, 0, 0, 1, 0, 0, 2*np.pi)
rev = np.transpose(rev)
sh.occ.synchronize()

s = rev[1, np.argwhere(rev[0]==2).flatten()]
s = np.append(s, y[0:1])

# Physical boundary

sh.addPhysicalGroup(3, [x], name='Fluid')
sh.addPhysicalGroup(2, k, name='FSInterface')
sh.addPhysicalGroup(2, y[1:2], name='FreeSurface')
sh.addPhysicalGroup(2, y[2:3], name='Inlet')
sh.addPhysicalGroup(2, s, name='Border')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(3)
gmsh.write(os.path.dirname(__file__)+'/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()
