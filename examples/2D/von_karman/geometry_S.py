import os, gmsh
import numpy as np
from gmsh import model as sh
gmsh.initialize()

# Mesh Parameters

L = 1
H = 0.41
R = 0.05
CX = 0.2
CY = 0.2
BX = 0.6
BH = 0.01

d = 4e-3
N = 101
M = 7

# Points list

p = list()
A = np.sqrt(np.square(R)-np.square(BH))

p.append(sh.occ.addPoint(BX, CY-BH, 0, d))
p.append(sh.occ.addPoint(BX, CY+BH, 0, d))
p.append(sh.occ.addPoint(CX+A, CY-BH, 0, d))
p.append(sh.occ.addPoint(CX+A, CY+BH, 0, d))

# Lines list

l = list()

l.append(sh.occ.addLine(p[2], p[0]))
l.append(sh.occ.addLine(p[0], p[1]))
l.append(sh.occ.addLine(p[1], p[3]))
l.append(sh.occ.addLine(p[3], p[2]))

# Physical surface

k = sh.occ.addCurveLoop(l)
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(l[0], N)
sh.mesh.setTransfiniteCurve(l[1], M)
sh.mesh.setTransfiniteCurve(l[2], N)
sh.mesh.setTransfiniteCurve(l[3], M)

sh.mesh.setTransfiniteSurface(s)
sh.mesh.setRecombine(2, s)

# Physical boundary

sh.addPhysicalGroup(2, [s], name='Solid')
sh.addPhysicalGroup(1, l[3:4], name='Clamped')
sh.addPhysicalGroup(1, l[:3], name='FSI')

# Write the mesh file

sh.mesh.generate(2)
gmsh.option.setNumber('Mesh.SaveParametric', 1)
gmsh.write(f'{os.path.dirname(__file__)}/geometry_S.msh')
gmsh.fltk.run()
gmsh.finalize()