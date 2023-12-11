import os,gmsh
import numpy as np
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

R = 2.25
H = 3.75
B = 4.87
h = 2.5
b = 1.3

# Characteristic size

d = 0.05
N = 160
M = 80

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(-B/2,H+h,0,d))
p.append(sh.occ.addPoint(-b/2,H,0,d))
p.append(sh.occ.addPoint(-R,H,0,d))
p.append(sh.occ.addPoint(-R,0,0,d))
p.append(sh.occ.addPoint(B/2,H+h,0,d))
p.append(sh.occ.addPoint(b/2,H,0,d))
p.append(sh.occ.addPoint(R,H,0,d))
p.append(sh.occ.addPoint(R,0,0,d))
p.append(sh.occ.addPoint(0,0,0,d))

# Lines List

l = list()

l.append(sh.occ.addLine(p[3],p[2]))
l.append(sh.occ.addLine(p[6],p[7]))
l.append(sh.occ.addCircleArc(p[7],p[8],p[3]))
l.append(sh.occ.addLine(p[0],p[1]))
l.append(sh.occ.addLine(p[1],p[5]))
l.append(sh.occ.addLine(p[5],p[4]))
l.append(sh.occ.addLine(p[4],p[0]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop(l[3:])
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(l[0],M)
sh.mesh.setTransfiniteCurve(l[1],M)
sh.mesh.setTransfiniteCurve(l[2],N)

# Physical Boundary

sh.addPhysicalGroup(2,[s],name='Fluid')
sh.addPhysicalGroup(1,l[:3],name='FSInterface')
sh.addPhysicalGroup(1,[l[3],l[5]],name='Reservoir')
sh.addPhysicalGroup(1,[l[4],l[6]],name='FreeSurface')

# |----------------------------------------|
# |   Mesh Characteristic Size Function    |
# |----------------------------------------|

fun = str(d)+'+0.3*F1'
sh.mesh.field.add('Distance',1)
sh.mesh.field.setNumber(1,'Sampling',1e4)
sh.mesh.field.setNumbers(1,'CurvesList',l)

sh.mesh.field.add('MathEval',2)
sh.mesh.field.setString(2,'F',fun)

sh.mesh.field.setAsBackgroundMesh(2)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints',0)
gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary',0)

# Write the Mesh File

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__)+'/geometryF.msh')
gmsh.fltk.run()
gmsh.finalize()