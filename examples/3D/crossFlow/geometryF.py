import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# %% Parameters

H = 0.4
B = 0.25
L1 = 0.15
L2 = 0.2

BS = 0.02
HS = 0.1
W = 0.005

d = 2e-3
N = 40
M = 10
P = 4

# %% Point List

p = list()

p.append(sh.occ.addPoint(0,0,0,d))
p.append(sh.occ.addPoint(L1+L2,0,0,d))
p.append(sh.occ.addPoint(L1+L2,B,0,d))
p.append(sh.occ.addPoint(0,B,0,d))
p.append(sh.occ.addPoint(0,0,H,d))
p.append(sh.occ.addPoint(L1+L2,0,H,d))
p.append(sh.occ.addPoint(L1+L2,B,H,d))
p.append(sh.occ.addPoint(0,B,H,d))

p.append(sh.occ.addPoint(L1,(B-BS)/2,0,d))
p.append(sh.occ.addPoint(L1+W,(B-BS)/2,0,d))
p.append(sh.occ.addPoint(L1+W,(B+BS)/2,0,d))
p.append(sh.occ.addPoint(L1,(B+BS)/2,0,d))
p.append(sh.occ.addPoint(L1,(B-BS)/2,HS,d))
p.append(sh.occ.addPoint(L1+W,(B-BS)/2,HS,d))
p.append(sh.occ.addPoint(L1+W,(B+BS)/2,HS,d))
p.append(sh.occ.addPoint(L1,(B+BS)/2,HS,d))

# %% Line List

l = list()

l.append(sh.occ.addLine(p[0],p[1]))
l.append(sh.occ.addLine(p[1],p[2]))
l.append(sh.occ.addLine(p[2],p[3]))
l.append(sh.occ.addLine(p[3],p[0]))
l.append(sh.occ.addLine(p[4],p[5]))
l.append(sh.occ.addLine(p[5],p[6]))
l.append(sh.occ.addLine(p[6],p[7]))
l.append(sh.occ.addLine(p[7],p[4]))

l.append(sh.occ.addLine(p[8],p[9]))
l.append(sh.occ.addLine(p[9],p[10]))
l.append(sh.occ.addLine(p[10],p[11]))
l.append(sh.occ.addLine(p[8],p[11]))
l.append(sh.occ.addLine(p[12],p[13]))
l.append(sh.occ.addLine(p[13],p[14]))
l.append(sh.occ.addLine(p[14],p[15]))
l.append(sh.occ.addLine(p[15],p[12]))

l.append(sh.occ.addLine(p[0],p[4]))
l.append(sh.occ.addLine(p[1],p[5]))
l.append(sh.occ.addLine(p[2],p[6]))
l.append(sh.occ.addLine(p[3],p[7]))
l.append(sh.occ.addLine(p[8],p[12]))
l.append(sh.occ.addLine(p[9],p[13]))
l.append(sh.occ.addLine(p[10],p[14]))
l.append(sh.occ.addLine(p[11],p[15]))

# %% Surface List

k = list()
s = list()

k.append(sh.occ.addCurveLoop([l[11],l[10],l[9],l[8]]))
k.append(sh.occ.addCurveLoop([l[8],l[21],l[12],l[20]]))
k.append(sh.occ.addCurveLoop([l[9],l[22],l[13],l[21]]))
k.append(sh.occ.addCurveLoop([l[20],l[15],l[23],l[11]]))
k.append(sh.occ.addCurveLoop([l[23],l[14],l[22],l[10]]))
k.append(sh.occ.addCurveLoop([l[12],l[13],l[14],l[15]]))

k.append(sh.occ.addCurveLoop([l[0],l[17],l[4],l[16]]))
k.append(sh.occ.addCurveLoop([l[2],l[19],l[6],l[18]]))
k.append(sh.occ.addCurveLoop([l[1],l[18],l[5],l[17]]))
k.append(sh.occ.addCurveLoop([l[3],l[16],l[7],l[19]]))
k.append(sh.occ.addCurveLoop([l[4],l[5],l[6],l[7]]))
k.append(sh.occ.addCurveLoop([l[3],l[2],l[1],l[0]]))

for a in k[:11]: s.append(sh.occ.addPlaneSurface([a]))
s.append(sh.occ.addPlaneSurface([k[11],-k[0]]))
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(l[20],N)
sh.mesh.setTransfiniteCurve(l[21],N)
sh.mesh.setTransfiniteCurve(l[22],N)
sh.mesh.setTransfiniteCurve(l[23],N)

sh.mesh.setTransfiniteCurve(l[9],M)
sh.mesh.setTransfiniteCurve(l[11],M)
sh.mesh.setTransfiniteCurve(l[13],M)
sh.mesh.setTransfiniteCurve(l[15],M)

sh.mesh.setTransfiniteCurve(l[8],P)
sh.mesh.setTransfiniteCurve(l[10],P)
sh.mesh.setTransfiniteCurve(l[12],P)
sh.mesh.setTransfiniteCurve(l[14],P)

# %% Fluid Volume

h = sh.occ.addSurfaceLoop(s[1:])
v = sh.occ.addVolume([h])
sh.occ.synchronize()

# %% Physical Surface

sh.addPhysicalGroup(3,[v],name='Fluid')
sh.addPhysicalGroup(2,s[:6],name='Polytope')
sh.addPhysicalGroup(2,s[1:6],name='FSInterface')
sh.addPhysicalGroup(2,[s[0],s[11]],name='Bottom')
sh.addPhysicalGroup(2,[s[6],s[7],s[10]],name='Wall')
sh.addPhysicalGroup(2,[s[8]],name='Outlet')
sh.addPhysicalGroup(2,[s[9]],name='Inlet')

# %% Mesh Size Function

def meshSize(dim,tag,x,y,z,lc):

    F = 0.1
    size = list()
    size.append(max(d+F*(z-HS),d))
    size.append(max(d+F*(L1-x),d))
    size.append(max(d+F*(x-L1-W),d))
    size.append(max(d+F*(y-(B+BS)/2),d))
    size.append(max(d+F*((B-BS)/2-y),d))
    return max(size)
    
sh.mesh.setSizeCallback(meshSize)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints',0)
gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary',0)

# %% Save the Mesh

sh.mesh.generate(3)
gmsh.option.setNumber('Mesh.Binary',1)
gmsh.write(os.path.dirname(__file__)+'/geometryF.msh')
gmsh.fltk.run()
gmsh.finalize()