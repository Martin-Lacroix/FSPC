import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# %% Parameters

H = 0.079
S = 0.005
D = 0.14
L1 = 0.1
L2 = 0.1

d = 1e-3
eps = 1e-5
N = 80

# %% Point List

p = list()

p.append(sh.occ.addPoint(0,0,0,d))
p.append(sh.occ.addPoint(L1,0,0,d))
p.append(sh.occ.addPoint(L1+S+L2,0,0,d))
p.append(sh.occ.addPoint(0,D,0,d))
p.append(sh.occ.addPoint(L1,D,0,d))
p.append(sh.occ.addPoint(L1,H,0,d))
p.append(sh.occ.addPoint(L1,eps,0,d))

# %% Line List

l = list()

l.append(sh.occ.addLine(p[0],p[1]))
l.append(sh.occ.addLine(p[1],p[6]))
l.append(sh.occ.addLine(p[5],p[6]))
l.append(sh.occ.addLine(p[4],p[5]))
l.append(sh.occ.addLine(p[4],p[3]))
l.append(sh.occ.addLine(p[3],p[0]))
l.append(sh.occ.addLine(p[1],p[2]))

# %% Fluid Mesh

k = sh.occ.addCurveLoop(l[:6])
s = sh.occ.addPlaneSurface([k])

sh.occ.synchronize()
sh.mesh.setTransfiniteCurve(l[2],N)

# %% Boundary Domains

sh.addPhysicalGroup(2,[s],name='Fluid')
sh.addPhysicalGroup(1,[l[4]],name='FreeSurface')
sh.addPhysicalGroup(1,[l[2]],name='FSInterface')
sh.addPhysicalGroup(1,[l[0],l[3]]+l[5:7],name='Reservoir')

# %% Mesh Size Function

def meshSize(dim,tag,x,y,z,lc):

    F = 0.2
    size = list()
    size.append(max(d+F*x,d))
    size.append(max(d+F*y,d))
    size.append(max(d+F*(L1-x),d))
    size.append(max(d+F*(D-y),d))
    return min(size)
    
sh.mesh.setSizeCallback(meshSize)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints',0)
gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary',0)

# %% Save the Mesh

sh.mesh.generate(2)
gmsh.option.setNumber('Mesh.Binary',1)
gmsh.write(os.path.dirname(__file__)+'/geometryF.msh')
gmsh.fltk.run()
gmsh.finalize()