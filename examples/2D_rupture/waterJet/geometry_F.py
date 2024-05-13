import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

HS = 1
LS = 2
LF = 0.1
HF = 1.2

d = 0.01
N = 101
M = 201

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(-LF/2, HF, 0, d))
p.append(sh.occ.addPoint(LF/2, HF, 0, d))
p.append(sh.occ.addPoint(LF/2, HF + LF, 0, d))
p.append(sh.occ.addPoint(-LF/2, HF + LF, 0, d))

p.append(sh.occ.addPoint(LS/2, HS, 0, d))
p.append(sh.occ.addPoint(-LS/2, HS, 0, d))
p.append(sh.occ.addPoint(-LS/2, 0, 0, d))
p.append(sh.occ.addPoint(LS/2, 0, 0, d))

# Lines List

l = list()
h = list()

l.append(sh.occ.addLine(p[0], p[1]))
l.append(sh.occ.addLine(p[1], p[2]))
l.append(sh.occ.addLine(p[2], p[3]))
l.append(sh.occ.addLine(p[3], p[0]))

h.append(sh.occ.addLine(p[4], p[5]))
h.append(sh.occ.addLine(p[5], p[6]))
h.append(sh.occ.addLine(p[6], p[7]))
h.append(sh.occ.addLine(p[7], p[4]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop(l)
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(h[0], M)
sh.mesh.setTransfiniteCurve(h[1], N)
sh.mesh.setTransfiniteCurve(h[2], M)
sh.mesh.setTransfiniteCurve(h[3], N)

# Physical Boundary

sh.addPhysicalGroup(2, [s], name='Fluid')
sh.addPhysicalGroup(1, [l[0], l[1], l[3]], name='FreeSurface')
sh.addPhysicalGroup(1, l[2:3], name='Inlet')
sh.addPhysicalGroup(1, h, name='FSInterface')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__) + '/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()