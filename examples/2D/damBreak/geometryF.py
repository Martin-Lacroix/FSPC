import os,gmsh
from gmsh import model as sh
gmsh.initialize()

# |---------------------------|
# |   Mesh Size Parameters    |
# |---------------------------|

L = 0.146
w = 0.012
h = 0.08
d = 0.005

N = 16
M = 4

# |----------------------------------|
# |   Points and Lines Definition    |
# |----------------------------------|

p = list()

p.append(sh.occ.addPoint(0,0,0,d))
p.append(sh.occ.addPoint(4*L,0,0,d))
p.append(sh.occ.addPoint(4*L,4*L,0,d))
p.append(sh.occ.addPoint(0,3*L,0,d))
p.append(sh.occ.addPoint(L,0,0,d))
p.append(sh.occ.addPoint(L,2*L,0,d))
p.append(sh.occ.addPoint(0,2*L,0,d))
p.append(sh.occ.addPoint(2*L,0,0,d))
p.append(sh.occ.addPoint(2*L,h,0,d))
p.append(sh.occ.addPoint(2*L+w,h,0,d))
p.append(sh.occ.addPoint(2*L+w,0,0,d))

# Lines List

l = list()
h = list()

l.append(sh.occ.addLine(p[3],p[6]))
l.append(sh.occ.addLine(p[6],p[0]))
l.append(sh.occ.addLine(p[0],p[4]))
l.append(sh.occ.addLine(p[4],p[5]))
l.append(sh.occ.addLine(p[5],p[6]))
l.append(sh.occ.addLine(p[4],p[7]))
l.append(sh.occ.addLine(p[10],p[1]))
l.append(sh.occ.addLine(p[1],p[2]))

h.append(sh.occ.addLine(p[7],p[8]))
h.append(sh.occ.addLine(p[8],p[9]))
h.append(sh.occ.addLine(p[9],p[10]))
h.append(sh.occ.addLine(p[7],p[10]))

# |------------------------------------|
# |   Physical Surface and Boundary    |
# |------------------------------------|

k = sh.occ.addCurveLoop(l[1:5])
s = sh.occ.addPlaneSurface([k])
sh.occ.synchronize()

sh.mesh.setTransfiniteCurve(h[0],N)
sh.mesh.setTransfiniteCurve(h[1],M)
sh.mesh.setTransfiniteCurve(h[2],N)
sh.mesh.setTransfiniteCurve(h[3],M)

# Physical Boundary

sh.addPhysicalGroup(2,[s],name='Fluid')
sh.addPhysicalGroup(1,h[0:3],name='FSInterface')
sh.addPhysicalGroup(1,l[0:3]+l[5:]+[h[3]],name='Reservoir')
sh.addPhysicalGroup(1,l[3:5],name='FreeSurface')
sh.addPhysicalGroup(1,h,name='Polytope')

# |----------------------------------------|
# |   Mesh Characteristic Size Function    |
# |----------------------------------------|

def meshSize(dim,tag,x,y,z,lc):

    F = 0.1
    size = list()
    size.append(max(d+F*x,d))
    size.append(max(d+F*y,d))
    size.append(max(d+F*(L-x),d))
    size.append(max(d+F*(2*L-y),d))
    return min(size)
    
sh.mesh.setSizeCallback(meshSize)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints',0)
gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary',0)

# Write the Mesh File

sh.mesh.generate(2)
gmsh.write(os.path.dirname(__file__)+'/geometryF.msh')
gmsh.fltk.run()
gmsh.finalize()