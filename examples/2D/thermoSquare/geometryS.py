import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# %% Parameters

R = 2
d = 0.05
N = 101

# %% Points List

p = list()

p.append(sh.occ.addPoint(-R,-R,0,d))
p.append(sh.occ.addPoint(R,-R,0,d))
p.append(sh.occ.addPoint(R,R,0,d))
p.append(sh.occ.addPoint(-R,R,0,d))

# %% Lines List

l = list()

l.append(sh.occ.addLine(p[0],p[1]))
l.append(sh.occ.addLine(p[1],p[2]))
l.append(sh.occ.addLine(p[2],p[3]))
l.append(sh.occ.addLine(p[3],p[0]))

# %% Solid Surface

k = sh.occ.addCurveLoop(l)
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(l[0],N)
sh.mesh.setTransfiniteCurve(l[1],N)
sh.mesh.setTransfiniteCurve(l[2],N)
sh.mesh.setTransfiniteCurve(l[3],N)

sh.mesh.setTransfiniteSurface(s)
sh.mesh.setRecombine(2,s)

# %% Physical Boundary

sh.addPhysicalGroup(2,[s],name='Solid')
sh.addPhysicalGroup(1,l,name='FSInterface')

# %% Save the Mesh

sh.mesh.generate(2)
gmsh.option.setNumber('Mesh.Binary',1)
gmsh.write(os.path.dirname(__file__)+'/geometryS.msh')
gmsh.fltk.run()
gmsh.finalize()