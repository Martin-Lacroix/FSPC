import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

H = 0.079
S = 0.005
D = 0.14
L1 = 0.1
L2 = 0.1

# Characteristic size

d = 1e-3
eps = 1e-5
N = 80

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(0, 0, 0, d))
p.append(sh.occ.addPoint(L1, 0, 0, d))
p.append(sh.occ.addPoint(L1 + S + L2, 0, 0, d))
p.append(sh.occ.addPoint(0, D, 0, d))
p.append(sh.occ.addPoint(L1, D, 0, d))
p.append(sh.occ.addPoint(L1, H, 0, d))
p.append(sh.occ.addPoint(L1, eps, 0, d))

# Lines List

l = list()

l.append(sh.occ.addLine(p[0], p[1]))
l.append(sh.occ.addLine(p[1], p[6]))
l.append(sh.occ.addLine(p[5], p[6]))
l.append(sh.occ.addLine(p[4], p[5]))
l.append(sh.occ.addLine(p[4], p[3]))
l.append(sh.occ.addLine(p[3], p[0]))
l.append(sh.occ.addLine(p[1], p[2]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop(l[:6])
s = sh.occ.addPlaneSurface([k])

sh.occ.synchronize()
sh.mesh.setTransfiniteCurve(l[2], N)

# Boundary Domains

sh.addPhysicalGroup(2, [s], name='Fluid')
sh.addPhysicalGroup(1, l[4:5], name='FreeSurface')
sh.addPhysicalGroup(1, l[2:3], name='FSInterface')
sh.addPhysicalGroup(1, [l[0], l[3]] + l[5:7], name='Reservoir')

# |----------------------------------------|
# |   Mesh Characteristic Size Function    |
# |----------------------------------------|

fun = str(d) + ' + 0.2*F1'
sh.mesh.field.add('Distance', 1)
sh.mesh.field.setNumber(1, 'Sampling', 1e4)
sh.mesh.field.setNumbers(1, 'CurvesList', l)

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