import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

L = 5
R = 2

# Characteristic size

d = 0.05
N = 101

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(-L, -L, 0, d))
p.append(sh.occ.addPoint(L, -L, 0, d))
p.append(sh.occ.addPoint(L, L, 0, d))
p.append(sh.occ.addPoint(-L, L, 0, d))

p.append(sh.occ.addPoint(-R, -R, 0, d))
p.append(sh.occ.addPoint(R, -R, 0, d))
p.append(sh.occ.addPoint(R, R, 0, d))
p.append(sh.occ.addPoint(-R, R, 0, d))

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

k = list()

k.append(sh.occ.addCurveLoop(l))
k.append(sh.occ.addCurveLoop(h))
s = sh.occ.addPlaneSurface([k[0], -k[1]])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(h[0], N)
sh.mesh.setTransfiniteCurve(h[1], N)
sh.mesh.setTransfiniteCurve(h[2], N)
sh.mesh.setTransfiniteCurve(h[3], N)

# Boundaries

sh.addPhysicalGroup(2, [s], name='Fluid')
sh.addPhysicalGroup(1, h, name='FSInterface')
sh.addPhysicalGroup(1, l, name='Wall')

# |----------------------------------------|
# |   Mesh Characteristic Size Function    |
# |----------------------------------------|

fun = str(d) + ' + 0.1*F1'
sh.mesh.field.add('Distance', 1)
sh.mesh.field.setNumber(1, 'Sampling', 1e4)
sh.mesh.field.setNumbers(1, 'CurvesList', h)

sh.mesh.field.add('MathEval', 2)
sh.mesh.field.setString(2, 'F', fun)

sh.mesh.field.setAsBackgroundMesh(2)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 0)
gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary', 0)

# Write the Mesh File

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__) + '/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()