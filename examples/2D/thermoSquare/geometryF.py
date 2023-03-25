import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# %% Parameters

L = 5
R = 2
d = 0.05
N = 101

# %% Points List

p = list()

p.append(sh.occ.addPoint(-L,-L,0,d))
p.append(sh.occ.addPoint(L,-L,0,d))
p.append(sh.occ.addPoint(L,L,0,d))
p.append(sh.occ.addPoint(-L,L,0,d))

p.append(sh.occ.addPoint(-R,-R,0,d))
p.append(sh.occ.addPoint(R,-R,0,d))
p.append(sh.occ.addPoint(R,R,0,d))
p.append(sh.occ.addPoint(-R,R,0,d))

# %% Lines List

l = list()
h = list()

l.append(sh.occ.addLine(p[0],p[1]))
l.append(sh.occ.addLine(p[1],p[2]))
l.append(sh.occ.addLine(p[2],p[3]))
l.append(sh.occ.addLine(p[3],p[0]))

h.append(sh.occ.addLine(p[4],p[5]))
h.append(sh.occ.addLine(p[5],p[6]))
h.append(sh.occ.addLine(p[6],p[7]))
h.append(sh.occ.addLine(p[7],p[4]))

# %% Fluid Surface

k = list()

k.append(sh.occ.addCurveLoop(l))
k.append(sh.occ.addCurveLoop(h))
s = sh.occ.addPlaneSurface([k[0],-k[1]])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(h[0],N)
sh.mesh.setTransfiniteCurve(h[1],N)
sh.mesh.setTransfiniteCurve(h[2],N)
sh.mesh.setTransfiniteCurve(h[3],N)

# %% Boundaries

sh.addPhysicalGroup(2,[s],name='Fluid')
sh.addPhysicalGroup(1,h,name='FSInterface')
sh.addPhysicalGroup(1,l,name='Wall')

# %% Mesh Size Function

def meshSize(dim,tag,x,y,z,lc):

    F = 0.1
    size = list()
    size.append(max(d+F*(abs(x)-R),d))
    size.append(max(d+F*(abs(y)-R),d))
    return max(size)
    
sh.mesh.setSizeCallback(meshSize)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints',0)
gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary',0)

# %% Save the Mesh

sh.mesh.generate(2)
gmsh.option.setNumber('Mesh.Binary',1)
gmsh.write(os.path.dirname(__file__)+'/geometryF.msh')
gmsh.fltk.run()
gmsh.finalize()