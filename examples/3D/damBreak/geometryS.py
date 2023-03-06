import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# %% Parameters

S = 0.6
Ly = 0.3
Sx = 0.03
Sy = 0.1
Sz = 0.3

N = 20
M = 10
P = 4

# %% Points List

p = list()

p.append(sh.occ.addPoint(S,(Ly-Sy)/2,0))
p.append(sh.occ.addPoint(S+Sx,(Ly-Sy)/2,0))
p.append(sh.occ.addPoint(S+Sx,(Ly+Sy)/2,0))
p.append(sh.occ.addPoint(S,(Ly+Sy)/2,0))

p.append(sh.occ.addPoint(S,(Ly-Sy)/2,Sz))
p.append(sh.occ.addPoint(S+Sx,(Ly-Sy)/2,Sz))
p.append(sh.occ.addPoint(S+Sx,(Ly+Sy)/2,Sz))
p.append(sh.occ.addPoint(S,(Ly+Sy)/2,Sz))

# %% Lines List

l = list()

l.append(sh.occ.addLine(p[0],p[1]))
l.append(sh.occ.addLine(p[1],p[2]))
l.append(sh.occ.addLine(p[2],p[3]))
l.append(sh.occ.addLine(p[0],p[3]))

l.append(sh.occ.addLine(p[4],p[5]))
l.append(sh.occ.addLine(p[5],p[6]))
l.append(sh.occ.addLine(p[6],p[7]))
l.append(sh.occ.addLine(p[7],p[4]))

l.append(sh.occ.addLine(p[0],p[4]))
l.append(sh.occ.addLine(p[1],p[5]))
l.append(sh.occ.addLine(p[2],p[6]))
l.append(sh.occ.addLine(p[3],p[7]))

# %% Surface List

k = list()
s = list()

k.append(sh.occ.addCurveLoop([l[3],l[2],l[1],l[0]]))
k.append(sh.occ.addCurveLoop([l[4],l[5],l[6],l[7]]))
k.append(sh.occ.addCurveLoop([l[0],l[9],l[4],l[8]]))
k.append(sh.occ.addCurveLoop([l[11],l[6],l[10],l[2]]))
k.append(sh.occ.addCurveLoop([l[1],l[10],l[5],l[9]]))
k.append(sh.occ.addCurveLoop([l[8],l[7],l[11],l[3]]))

for a in k: s.append(sh.occ.addPlaneSurface([a]))
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(l[8],N)
sh.mesh.setTransfiniteCurve(l[9],N)
sh.mesh.setTransfiniteCurve(l[10],N)
sh.mesh.setTransfiniteCurve(l[11],N)

sh.mesh.setTransfiniteCurve(l[1],M)
sh.mesh.setTransfiniteCurve(l[3],M)
sh.mesh.setTransfiniteCurve(l[5],M)
sh.mesh.setTransfiniteCurve(l[7],M)

sh.mesh.setTransfiniteCurve(l[0],P)
sh.mesh.setTransfiniteCurve(l[2],P)
sh.mesh.setTransfiniteCurve(l[4],P)
sh.mesh.setTransfiniteCurve(l[6],P)

for a in s: sh.mesh.setTransfiniteSurface(a)
for a in s: sh.mesh.setRecombine(2,a)

# %% Solid Volume

h = sh.occ.addSurfaceLoop(s)
v = sh.occ.addVolume([h])

sh.occ.synchronize()
sh.mesh.setTransfiniteVolume(v)
sh.mesh.setRecombine(3,v)

# %% Physical Surface

sh.addPhysicalGroup(3,[v],name='Solid')
sh.addPhysicalGroup(2,[s[0]],name='Clamped')
sh.addPhysicalGroup(2,s[1:],name='FSInterface')

# %% Save the Mesh

sh.mesh.generate(3)
gmsh.option.setNumber('Mesh.Binary',1)
gmsh.write(os.path.dirname(__file__)+'/geometryS.msh')
gmsh.fltk.run()
gmsh.finalize()