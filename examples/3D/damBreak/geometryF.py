import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# |--------------------------|
# |   Mesh Size Parameters   |
# |--------------------------|

Lx = 1.1
Ly = 0.3
Lz = 0.4
Fx = 0.3

S = 0.6
Sx = 0.03
Sy = 0.1
Sz = 0.3

d = 0.01
N = 20
M = 10
P = 4

# |---------------------------------|
# |   Points and Lines Definition   |
# |---------------------------------|

p = list()

p.append(sh.occ.addPoint(0,0,0,d))
p.append(sh.occ.addPoint(Fx,0,0,d))
p.append(sh.occ.addPoint(Lx,0,0,d))
p.append(sh.occ.addPoint(Lx,0,Lz,d))
p.append(sh.occ.addPoint(Fx,0,Lz,d))
p.append(sh.occ.addPoint(0,0,Lz,d))

p.append(sh.occ.addPoint(0,Ly,0,d))
p.append(sh.occ.addPoint(Fx,Ly,0,d))
p.append(sh.occ.addPoint(Lx,Ly,0,d))
p.append(sh.occ.addPoint(Lx,Ly,Lz,d))
p.append(sh.occ.addPoint(Fx,Ly,Lz,d))
p.append(sh.occ.addPoint(0,Ly,Lz,d))

p.append(sh.occ.addPoint(S,(Ly-Sy)/2,0,d))
p.append(sh.occ.addPoint(S+Sx,(Ly-Sy)/2,0,d))
p.append(sh.occ.addPoint(S+Sx,(Ly+Sy)/2,0,d))
p.append(sh.occ.addPoint(S,(Ly+Sy)/2,0,d))

p.append(sh.occ.addPoint(S,(Ly-Sy)/2,Sz,d))
p.append(sh.occ.addPoint(S+Sx,(Ly-Sy)/2,Sz,d))
p.append(sh.occ.addPoint(S+Sx,(Ly+Sy)/2,Sz,d))
p.append(sh.occ.addPoint(S,(Ly+Sy)/2,Sz,d))

# Lines List

l = list()

l.append(sh.occ.addLine(p[0],p[1]))
l.append(sh.occ.addLine(p[1],p[2]))
l.append(sh.occ.addLine(p[2],p[3]))
l.append(sh.occ.addLine(p[3],p[4]))
l.append(sh.occ.addLine(p[4],p[5]))
l.append(sh.occ.addLine(p[5],p[0]))

l.append(sh.occ.addLine(p[6],p[7]))
l.append(sh.occ.addLine(p[7],p[8]))
l.append(sh.occ.addLine(p[8],p[9]))
l.append(sh.occ.addLine(p[9],p[10]))
l.append(sh.occ.addLine(p[10],p[11]))
l.append(sh.occ.addLine(p[11],p[6]))

l.append(sh.occ.addLine(p[0],p[6]))
l.append(sh.occ.addLine(p[1],p[7]))
l.append(sh.occ.addLine(p[2],p[8]))
l.append(sh.occ.addLine(p[3],p[9]))
l.append(sh.occ.addLine(p[4],p[10]))
l.append(sh.occ.addLine(p[5],p[11]))

l.append(sh.occ.addLine(p[1],p[4]))
l.append(sh.occ.addLine(p[7],p[10]))

l.append(sh.occ.addLine(p[12],p[13]))
l.append(sh.occ.addLine(p[13],p[14]))
l.append(sh.occ.addLine(p[14],p[15]))
l.append(sh.occ.addLine(p[12],p[15]))

l.append(sh.occ.addLine(p[16],p[17]))
l.append(sh.occ.addLine(p[17],p[18]))
l.append(sh.occ.addLine(p[18],p[19]))
l.append(sh.occ.addLine(p[19],p[16]))

l.append(sh.occ.addLine(p[12],p[16]))
l.append(sh.occ.addLine(p[13],p[17]))
l.append(sh.occ.addLine(p[14],p[18]))
l.append(sh.occ.addLine(p[15],p[19]))

# |-------------------------------------|
# |   Surfaces and Volumes Definition   |
# |-------------------------------------|

k = list()
s = list()

k.append(sh.occ.addCurveLoop([l[0],l[18],l[4],l[5]]))
k.append(sh.occ.addCurveLoop([l[0],l[13],l[6],l[12]]))
k.append(sh.occ.addCurveLoop([l[6],l[19],l[10],l[11]]))
k.append(sh.occ.addCurveLoop([l[4],l[16],l[10],l[17]]))
k.append(sh.occ.addCurveLoop([l[5],l[12],l[11],l[17]]))
k.append(sh.occ.addCurveLoop([l[18],l[13],l[19],l[16]]))

k.append(sh.occ.addCurveLoop([l[23],l[22],l[21],l[20]]))
k.append(sh.occ.addCurveLoop([l[24],l[25],l[26],l[27]]))
k.append(sh.occ.addCurveLoop([l[20],l[29],l[24],l[28]]))
k.append(sh.occ.addCurveLoop([l[31],l[26],l[30],l[22]]))
k.append(sh.occ.addCurveLoop([l[21],l[30],l[25],l[29]]))
k.append(sh.occ.addCurveLoop([l[28],l[27],l[31],l[23]]))

k.append(sh.occ.addCurveLoop([l[1],l[2],l[3],l[18]]))
k.append(sh.occ.addCurveLoop([l[7],l[8],l[9],l[19]]))
k.append(sh.occ.addCurveLoop([l[14],l[8],l[15],l[2]]))
k.append(sh.occ.addCurveLoop([l[1],l[14],l[7],l[13]]))

for a in k[:16]: s.append(sh.occ.addPlaneSurface([a]))
s.append(sh.occ.addPlaneSurface([k[15],-k[6]]))
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(l[28],N)
sh.mesh.setTransfiniteCurve(l[29],N)
sh.mesh.setTransfiniteCurve(l[30],N)
sh.mesh.setTransfiniteCurve(l[31],N)

sh.mesh.setTransfiniteCurve(l[21],M)
sh.mesh.setTransfiniteCurve(l[23],M)
sh.mesh.setTransfiniteCurve(l[25],M)
sh.mesh.setTransfiniteCurve(l[27],M)

sh.mesh.setTransfiniteCurve(l[20],P)
sh.mesh.setTransfiniteCurve(l[22],P)
sh.mesh.setTransfiniteCurve(l[24],P)
sh.mesh.setTransfiniteCurve(l[26],P)

# Volumes List

h = sh.occ.addSurfaceLoop(s[:6])
v = sh.occ.addVolume([h])
sh.occ.synchronize()

# Physical Surface

sh.addPhysicalGroup(3,[v],name='Fluid')
sh.addPhysicalGroup(2,s[6:12],name='Polytope')
sh.addPhysicalGroup(2,s[7:12],name='FSInterface')
sh.addPhysicalGroup(2,[s[3],s[5]],name='FreeSurface')
sh.addPhysicalGroup(2,s[:3]+[s[4]]+s[12:],name='Reservoir')

# |---------------------------------------|
# |   Mesh Characteristic Size Function   |
# |---------------------------------------|

def meshSize(dim,tag,x,y,z,lc):

    F = 0.4
    size = list()
    size.append(max(d+F*x,d))
    size.append(max(d+F*y,d))
    size.append(max(d+F*z,d))
    size.append(max(d+F*(Fx-x),d))
    size.append(max(d+F*(Ly-y),d))
    size.append(max(d+F*(Lz-z),d))
    return min(size)
    
sh.mesh.setSizeCallback(meshSize)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints',0)
gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary',0)

# Write the Mesh File

sh.mesh.generate(3)
gmsh.write(os.path.dirname(__file__)+'/geometryF.msh')
gmsh.fltk.run()
gmsh.finalize()