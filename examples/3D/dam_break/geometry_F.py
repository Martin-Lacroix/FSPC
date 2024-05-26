import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

S = 0.15
L = 0.146
R = 0.015
A = 2*L
H = 2*L
W = L/2

# Characteristic size

d = 0.005

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(0, -W, 0, d))
p.append(sh.occ.addPoint(L, -W, 0, d))
p.append(sh.occ.addPoint(L, W, 0, d))
p.append(sh.occ.addPoint(0, W, 0, d))
p.append(sh.occ.addPoint(0, -W, H, d))
p.append(sh.occ.addPoint(L, -W, H, d))
p.append(sh.occ.addPoint(L, W, H, d))
p.append(sh.occ.addPoint(0, W, H, d))

p.append(sh.occ.addPoint(4*L, -W, 0, d))
p.append(sh.occ.addPoint(4*L, W, 0, d))
p.append(sh.occ.addPoint(4*L, -W, H, d))
p.append(sh.occ.addPoint(4*L, W, H, d))

p.append(sh.occ.addPoint(A, -W, 0, d))
p.append(sh.occ.addPoint(A, -R, 0, d))
p.append(sh.occ.addPoint(A, 0, 0, d))
p.append(sh.occ.addPoint(A, R, 0, d))
p.append(sh.occ.addPoint(A, W, 0, d))

p.append(sh.occ.addPoint(A, -R, S, d))
p.append(sh.occ.addPoint(A, 0, S, d))
p.append(sh.occ.addPoint(A, R, S, d))

# Lines list

l = list()

l.append(sh.occ.addLine(p[0], p[1]))
l.append(sh.occ.addLine(p[1], p[2]))
l.append(sh.occ.addLine(p[2], p[3]))
l.append(sh.occ.addLine(p[3], p[0]))

l.append(sh.occ.addLine(p[4], p[5]))
l.append(sh.occ.addLine(p[5], p[6]))
l.append(sh.occ.addLine(p[6], p[7]))
l.append(sh.occ.addLine(p[7], p[4]))

l.append(sh.occ.addLine(p[0], p[4]))
l.append(sh.occ.addLine(p[1], p[5]))
l.append(sh.occ.addLine(p[2], p[6]))
l.append(sh.occ.addLine(p[3], p[7]))

l.append(sh.occ.addLine(p[8], p[9]))
l.append(sh.occ.addLine(p[9], p[11]))
l.append(sh.occ.addLine(p[11], p[10]))
l.append(sh.occ.addLine(p[10], p[8]))

l.append(sh.occ.addLine(p[1], p[12]))
l.append(sh.occ.addLine(p[2], p[16]))
l.append(sh.occ.addLine(p[12], p[8]))
l.append(sh.occ.addLine(p[16], p[9]))
l.append(sh.occ.addLine(p[5], p[10]))
l.append(sh.occ.addLine(p[6], p[11]))

l.append(sh.occ.addLine(p[12], p[13]))
l.append(sh.occ.addLine(p[15], p[16]))
l.append(sh.occ.addLine(p[13], p[17]))
l.append(sh.occ.addLine(p[15], p[19]))

l.append(sh.occ.addCircleArc(p[13], p[14], p[15]))
l.append(sh.occ.addCircleArc(p[15], p[14], p[13]))
l.append(sh.occ.addCircleArc(p[17], p[18], p[19]))
l.append(sh.occ.addCircleArc(p[19], p[18], p[17]))

# |--------------------------------------|
# |   Surfaces and Volumes Definition    |
# |--------------------------------------|

k = list()
s = list()
g = list()

k.append(sh.occ.addCurveLoop([l[0], l[1], l[2], l[3]]))
k.append(sh.occ.addCurveLoop([l[4], l[5], l[6], l[7]]))
k.append(sh.occ.addCurveLoop([l[0], l[9], l[4], l[8]]))
k.append(sh.occ.addCurveLoop([l[3], l[11], l[7], l[8]]))
k.append(sh.occ.addCurveLoop([l[1], l[10], l[5], l[9]]))
k.append(sh.occ.addCurveLoop([l[2], l[10], l[6], l[11]]))

k.append(sh.occ.addCurveLoop([l[28], l[29]]))
k.append(sh.occ.addCurveLoop([l[1], l[16], l[22], l[26], l[23], l[17]]))
k.append(sh.occ.addCurveLoop([l[22], l[18], l[12], l[19], l[23], l[27]]))

k.append(sh.occ.addCurveLoop([l[12], l[13], l[14], l[15]]))
k.append(sh.occ.addCurveLoop([l[16], l[18], l[15], l[20], l[9]]))
k.append(sh.occ.addCurveLoop([l[17], l[19], l[13], l[21], l[10]]))

g.append(sh.occ.addCurveLoop([l[27], l[25], l[29], l[24]]))
g.append(sh.occ.addCurveLoop([l[26], l[25], l[28], l[24]]))

for a in k: s.append(sh.occ.addPlaneSurface([a]))
for a in g: s.append(sh.occ.addBSplineFilling(a))
sh.occ.synchronize()

# Volumes list

h = sh.occ.addSurfaceLoop(s[:6])
v = sh.occ.addVolume([h])
sh.occ.synchronize()

# Physical surface

sh.addPhysicalGroup(3, [v], name='Fluid')
sh.addPhysicalGroup(2, s[1:2]+s[4:5], name='FreeSurface')
sh.addPhysicalGroup(2, s[6:7]+s[12:13]+s[13:14], name='FSInterface')
sh.addPhysicalGroup(2, s[0:1]+s[2:3]+s[3:4]+s[5:6]+s[7:12], name='Reservoir')

# |----------------------------------------|
# |   Mesh Characteristic Size Function    |
# |----------------------------------------|

fun = str(d)+'+0.4*F1'
sh.mesh.field.add('Distance', 1)
sh.mesh.field.setNumber(1, 'Sampling', 1e3)
sh.mesh.field.setNumbers(1, 'SurfacesList', s)

sh.mesh.field.add('MathEval', 2)
sh.mesh.field.setString(2, 'F', fun)

sh.mesh.field.setAsBackgroundMesh(2)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 0)
gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary', 0)

# Write the mesh

sh.mesh.generate(3)
gmsh.write(os.path.dirname(__file__)+'/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()