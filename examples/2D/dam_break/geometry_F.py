import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

L = 0.146
w = 0.012
h = 0.08

# Characteristic size

d = 0.005
N = 18
M = 4

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(0, 0, 0, d))
p.append(sh.occ.addPoint(4*L, 0, 0, d))
p.append(sh.occ.addPoint(4*L, 4*L, 0, d))
p.append(sh.occ.addPoint(0, 3*L, 0, d))
p.append(sh.occ.addPoint(L, 0, 0, d))
p.append(sh.occ.addPoint(L, 2*L, 0, d))
p.append(sh.occ.addPoint(0, 2*L, 0, d))
p.append(sh.occ.addPoint(2*L, 0, 0, d))
p.append(sh.occ.addPoint(2*L, h, 0, d))
p.append(sh.occ.addPoint(2*L+w, h, 0, d))
p.append(sh.occ.addPoint(2*L+w, 0, 0, d))

# Lines list

l = list()
h = list()

l.append(sh.occ.addLine(p[3], p[6]))
l.append(sh.occ.addLine(p[6], p[0]))
l.append(sh.occ.addLine(p[0], p[4]))
l.append(sh.occ.addLine(p[4], p[5]))
l.append(sh.occ.addLine(p[5], p[6]))
l.append(sh.occ.addLine(p[4], p[7]))
l.append(sh.occ.addLine(p[10], p[1]))
l.append(sh.occ.addLine(p[1], p[2]))

h.append(sh.occ.addLine(p[7], p[8]))
h.append(sh.occ.addLine(p[8], p[9]))
h.append(sh.occ.addLine(p[9], p[10]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop(l[1:5])
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(h[0], N)
sh.mesh.setTransfiniteCurve(h[1], M)
sh.mesh.setTransfiniteCurve(h[2], N)

# Physical boundary

sh.addPhysicalGroup(2, [s], name='Fluid')
sh.addPhysicalGroup(1, h, name='FSInterface')
sh.addPhysicalGroup(1, l[0:3]+l[5:], name='Reservoir')
sh.addPhysicalGroup(1, l[3:5], name='FreeSurface')

# |----------------------------------------|
# |   Mesh Characteristic Size Function    |
# |----------------------------------------|

fun = str(d)+'+0.1*F1'
sh.mesh.field.add('Distance', 1)
sh.mesh.field.setNumber(1, 'Sampling', 1e4)
sh.mesh.field.setNumbers(1, 'CurvesList', l)

sh.mesh.field.add('MathEval', 2)
sh.mesh.field.setString(2, 'F', fun)

sh.mesh.field.setAsBackgroundMesh(2)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 0)
gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary', 0)

# Write the mesh

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__)+'/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()