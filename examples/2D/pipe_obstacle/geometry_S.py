import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# Mesh Parameters

L1 = 0.3
L2 = 0.5
L3 = 0.8

R1 = 0.3
R2 = 0.24

Y = -0.02
H = 0.05
L = 0.1
B = 0.2

R = 0.02
S = 0.04
W = 0.02

d = 0.005
E = 1e-3
N = 101
M = 5

# Points list

p = list()

p.append(sh.occ.addPoint(L1+L2-E-W, Y-R2, 0, d))
p.append(sh.occ.addPoint(L1+L2-E, Y-R2, 0, d))
p.append(sh.occ.addPoint(L1+L2-E, Y+R2, 0, d))
p.append(sh.occ.addPoint(L1+L2-E-W, Y+R2, 0, d))

# Lines list

l = list()

l.append(sh.occ.addLine(p[0], p[1]))
l.append(sh.occ.addLine(p[1], p[2]))
l.append(sh.occ.addLine(p[2], p[3]))
l.append(sh.occ.addLine(p[3], p[0]))

# Physical surface

k = sh.occ.addCurveLoop(l)
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(l[0], M)
sh.mesh.setTransfiniteCurve(l[1], N)
sh.mesh.setTransfiniteCurve(l[2], M)
sh.mesh.setTransfiniteCurve(l[3], N)

sh.mesh.setTransfiniteSurface(s)
sh.mesh.setRecombine(2, s)

# Physical boundary

sh.addPhysicalGroup(2, [s], name='Solid')
sh.addPhysicalGroup(1, l, name='FSI')

# Write the mesh file

sh.mesh.generate(2)
gmsh.write(f'{os.path.dirname(__file__)}/geometry_S.msh')
gmsh.fltk.run()
gmsh.finalize()