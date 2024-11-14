import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# Mesh Parameters

L = 0.146
W = 0.012
H = 0.08
d = 0.005

# Points list

p = list()

p.append(sh.occ.addPoint(0, 0, 0, d))
p.append(sh.occ.addPoint(4*L, 0, 0, d))
p.append(sh.occ.addPoint(4*L, 4*L, 0, d))
p.append(sh.occ.addPoint(0, 3*L, 0, d))
p.append(sh.occ.addPoint(L, 0, 0, d))
p.append(sh.occ.addPoint(L, 2*L, 0, d))
p.append(sh.occ.addPoint(0, 2*L, 0, d))
p.append(sh.occ.addPoint(2*L, 0, 0, d))
p.append(sh.occ.addPoint(2*L, H, 0, d))
p.append(sh.occ.addPoint(2*L+W, H, 0, d))
p.append(sh.occ.addPoint(2*L+W, 0, 0, d))

# Lines list

l = list()
H = list()

l.append(sh.occ.addLine(p[3], p[6]))
l.append(sh.occ.addLine(p[6], p[0]))
l.append(sh.occ.addLine(p[0], p[4]))
l.append(sh.occ.addLine(p[4], p[5]))
l.append(sh.occ.addLine(p[5], p[6]))
l.append(sh.occ.addLine(p[4], p[7]))
l.append(sh.occ.addLine(p[10], p[1]))
l.append(sh.occ.addLine(p[1], p[2]))

H.append(sh.occ.addLine(p[7], p[8]))
H.append(sh.occ.addLine(p[8], p[9]))
H.append(sh.occ.addLine(p[9], p[10]))

# Physical surface

k = sh.occ.addCurveLoop(l[1:5])
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

# Physical boundary

sh.addPhysicalGroup(2, [s], name='Fluid')
sh.addPhysicalGroup(1, H, name='FSInterface')
sh.addPhysicalGroup(1, l[0:3]+l[5:], name='Reservoir')

# Mesh characteristic size

sh.mesh.field.add('Distance', 1)
sh.mesh.field.setNumber(1, 'Sampling', 1e4)
sh.mesh.field.setNumbers(1, 'CurvesList', l+H)

sh.mesh.field.add('MathEval', 2)
sh.mesh.field.setString(2, 'F', f'{d}+0.1*F1')

sh.mesh.field.setAsBackgroundMesh(2)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 0)
gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary', 0)

# Write the mesh

sh.mesh.generate(2)
gmsh.write(f'{os.path.dirname(__file__)}/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()