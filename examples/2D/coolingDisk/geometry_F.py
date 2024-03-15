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
C = 0.2

# Characteristic size

d = 0.0075
N = 11

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(L, 0, 0, d))
p.append(sh.occ.addPoint(0, 0, 0, d))
p.append(sh.occ.addPoint(L, HF, 0, d))
p.append(sh.occ.addPoint(0, HF, 0, d))
p.append(sh.occ.addPoint(0, HF+HS+R, 0, d))
p.append(sh.occ.addPoint(L, HF+HS+R, 0, d))

p.append(sh.occ.addPoint(C, HF+HS, 0, d))
p.append(sh.occ.addPoint(C, HF+HS+R, 0, d))
p.append(sh.occ.addPoint(C, HF+HS-R, 0, d))

p.append(sh.occ.addPoint(L/2, HF+HS, 0, d))
p.append(sh.occ.addPoint(L/2, HF+HS+R, 0, d))
p.append(sh.occ.addPoint(L/2, HF+HS-R, 0, d))

p.append(sh.occ.addPoint(L-C, HF+HS, 0, d))
p.append(sh.occ.addPoint(L-C, HF+HS+R, 0, d))
p.append(sh.occ.addPoint(L-C, HF+HS-R, 0, d))

# Lines list

l = list()
h = list()
r = list()
u = list()

l.append(sh.occ.addLine(p[0], p[1]))
l.append(sh.occ.addLine(p[0], p[2]))
l.append(sh.occ.addLine(p[2], p[3]))
l.append(sh.occ.addLine(p[3], p[1]))
l.append(sh.occ.addLine(p[3], p[4]))
l.append(sh.occ.addLine(p[2], p[5]))

h.append(sh.occ.addCircleArc(p[7], p[6], p[8]))
h.append(sh.occ.addCircleArc(p[8], p[6], p[7]))

r.append(sh.occ.addCircleArc(p[10], p[9], p[11]))
r.append(sh.occ.addCircleArc(p[11], p[9], p[10]))

u.append(sh.occ.addCircleArc(p[13], p[12], p[14]))
u.append(sh.occ.addCircleArc(p[14], p[12], p[13]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop(l[:4])
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(h[0], N)
sh.mesh.setTransfiniteCurve(h[1], N)
sh.mesh.setTransfiniteCurve(r[0], N)
sh.mesh.setTransfiniteCurve(r[1], N)
sh.mesh.setTransfiniteCurve(u[0], N)
sh.mesh.setTransfiniteCurve(u[1], N)

# Physical boundary

sh.addPhysicalGroup(2, [s], name='Fluid')
sh.addPhysicalGroup(1, h+r+u, name='FSInterface')
sh.addPhysicalGroup(1, l[2:3], name='FreeSurface')
sh.addPhysicalGroup(1, l[:2]+l[3:], name='Wall')

# |--------------------------|
# |   Write the Mesh File    |
# |--------------------------|

sh.mesh.generate(2)
gmsh.model.mesh.reverse()
gmsh.write(os.path.dirname(__file__)+'/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()