import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# %% Parameters

L = 0.146
w = 0.012
h = 0.08

N = 40
M = 8

# %% Points List

p = list()

p.append(sh.occ.addPoint(2*L,0,0))
p.append(sh.occ.addPoint(2*L+w,0,0))
p.append(sh.occ.addPoint(2*L+w,h,0))
p.append(sh.occ.addPoint(2*L,h,0))

# %% Lines List

l = list()

l.append(sh.occ.addLine(p[0],p[1]))
l.append(sh.occ.addLine(p[1],p[2]))
l.append(sh.occ.addLine(p[2],p[3]))
l.append(sh.occ.addLine(p[3],p[0]))

# %% Solid Surface

k = sh.occ.addCurveLoop([l[0],l[1],l[2],l[3]])
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(l[0],M)
sh.mesh.setTransfiniteCurve(l[1],N)
sh.mesh.setTransfiniteCurve(l[2],M)
sh.mesh.setTransfiniteCurve(l[3],N)

sh.mesh.setTransfiniteSurface(s)
sh.mesh.setRecombine(2,s)

# %% Physical Boundary

sh.addPhysicalGroup(2,[s],name='Solid')
sh.addPhysicalGroup(1,l[1:4],name='FSInterface')
sh.addPhysicalGroup(1,[l[0]],name='SolidBase')

# %% Save the Mesh

sh.mesh.generate(2)
gmsh.option.setNumber('Mesh.Binary',1)
gmsh.write(os.path.dirname(__file__)+'/geometryS.msh')
gmsh.fltk.run()
gmsh.finalize()