import os, gmsh
from gmsh import model as sh
gmsh.initialize()

# Mesh Parameters

L = 0.609/2
W = 0.056/2
H = 0.3445

LS = 0.004/2
WS = 0.0332/2
HS = 0.1148

d = 5e-3

# Points list

p = list()

p.append(sh.occ.addPoint(-L, -W, 0, d))
p.append(sh.occ.addPoint(L, -W, 0, d))
p.append(sh.occ.addPoint(L, W, 0, d))
p.append(sh.occ.addPoint(-L, W, 0, d))

p.append(sh.occ.addPoint(-LS, -W, 0, d))
p.append(sh.occ.addPoint(LS, -W, 0, d))
p.append(sh.occ.addPoint(LS, W, 0, d))
p.append(sh.occ.addPoint(-LS, W, 0, d))

p.append(sh.occ.addPoint(-LS, -WS, 0, d))
p.append(sh.occ.addPoint(LS, -WS, 0, d))
p.append(sh.occ.addPoint(LS, WS, 0, d))
p.append(sh.occ.addPoint(-LS, WS, 0, d))

p.append(sh.occ.addPoint(-L, -W, HS, d))
p.append(sh.occ.addPoint(L, -W, HS, d))
p.append(sh.occ.addPoint(L, W, HS, d))
p.append(sh.occ.addPoint(-L, W, HS, d))

p.append(sh.occ.addPoint(-LS, -W, HS, d))
p.append(sh.occ.addPoint(LS, -W, HS, d))
p.append(sh.occ.addPoint(LS, W, HS, d))
p.append(sh.occ.addPoint(-LS, W, HS, d))

p.append(sh.occ.addPoint(-LS, -WS, HS, d))
p.append(sh.occ.addPoint(LS, -WS, HS, d))
p.append(sh.occ.addPoint(LS, WS, HS, d))
p.append(sh.occ.addPoint(-LS, WS, HS, d))

p.append(sh.occ.addPoint(-L, -W, H, d))
p.append(sh.occ.addPoint(L, -W, H, d))
p.append(sh.occ.addPoint(L, W, H, d))
p.append(sh.occ.addPoint(-L, W, H, d))

# Lines list

l = list()

l.append(sh.occ.addLine(p[0], p[4]))
l.append(sh.occ.addLine(p[4], p[5]))
l.append(sh.occ.addLine(p[5], p[1]))
l.append(sh.occ.addLine(p[1], p[2]))
l.append(sh.occ.addLine(p[2], p[6]))
l.append(sh.occ.addLine(p[6], p[7]))
l.append(sh.occ.addLine(p[7], p[3]))
l.append(sh.occ.addLine(p[3], p[0]))

l.append(sh.occ.addLine(p[4], p[8]))
l.append(sh.occ.addLine(p[5], p[9]))
l.append(sh.occ.addLine(p[6], p[10]))
l.append(sh.occ.addLine(p[7], p[11]))
l.append(sh.occ.addLine(p[8], p[11]))
l.append(sh.occ.addLine(p[8], p[9]))
l.append(sh.occ.addLine(p[9], p[10]))
l.append(sh.occ.addLine(p[10], p[11]))

l.append(sh.occ.addLine(p[12], p[16]))
l.append(sh.occ.addLine(p[16], p[17]))
l.append(sh.occ.addLine(p[17], p[13]))
l.append(sh.occ.addLine(p[13], p[14]))
l.append(sh.occ.addLine(p[14], p[18]))
l.append(sh.occ.addLine(p[18], p[19]))
l.append(sh.occ.addLine(p[19], p[15]))
l.append(sh.occ.addLine(p[15], p[12]))

l.append(sh.occ.addLine(p[16], p[20]))
l.append(sh.occ.addLine(p[17], p[21]))
l.append(sh.occ.addLine(p[18], p[22]))
l.append(sh.occ.addLine(p[19], p[23]))
l.append(sh.occ.addLine(p[20], p[23]))
l.append(sh.occ.addLine(p[20], p[21]))
l.append(sh.occ.addLine(p[21], p[22]))
l.append(sh.occ.addLine(p[22], p[23]))

l.append(sh.occ.addLine(p[24], p[25]))
l.append(sh.occ.addLine(p[25], p[26]))
l.append(sh.occ.addLine(p[26], p[27]))
l.append(sh.occ.addLine(p[27], p[24]))

l.append(sh.occ.addLine(p[0], p[12]))
l.append(sh.occ.addLine(p[1], p[13]))
l.append(sh.occ.addLine(p[2], p[14]))
l.append(sh.occ.addLine(p[3], p[15]))

l.append(sh.occ.addLine(p[12], p[24]))
l.append(sh.occ.addLine(p[13], p[25]))
l.append(sh.occ.addLine(p[14], p[26]))
l.append(sh.occ.addLine(p[15], p[27]))

l.append(sh.occ.addLine(p[8], p[20]))
l.append(sh.occ.addLine(p[9], p[21]))
l.append(sh.occ.addLine(p[10], p[22]))
l.append(sh.occ.addLine(p[11], p[23]))

# Surfaces list

k = list()
r = list()
sh.occ.synchronize()

k.append(sh.occ.addCurveLoop([l[0], l[8], l[12], l[11], l[6], l[7]]))
k.append(sh.occ.addCurveLoop([l[2], l[3], l[4], l[10], l[14], l[9]]))
k.append(sh.occ.addCurveLoop([l[11], l[5], l[10], l[15]]))
k.append(sh.occ.addCurveLoop([l[1], l[9], l[13], l[8]]))

k.append(sh.occ.addCurveLoop([l[16], l[24], l[28], l[27], l[22], l[23]]))
k.append(sh.occ.addCurveLoop([l[18], l[19], l[20], l[26], l[30], l[25]]))
k.append(sh.occ.addCurveLoop([l[27], l[31], l[26], l[21]]))
k.append(sh.occ.addCurveLoop([l[17], l[25], l[29], l[24]]))

k.append(sh.occ.addCurveLoop([l[13], l[45], l[29], l[44]]))
k.append(sh.occ.addCurveLoop([l[15], l[47], l[31], l[46]]))
k.append(sh.occ.addCurveLoop([l[14], l[46], l[30], l[45]]))
k.append(sh.occ.addCurveLoop([l[12], l[44], l[28], l[47]]))

k.append(sh.occ.addCurveLoop([l[36], l[23], l[39], l[7]]))
k.append(sh.occ.addCurveLoop([l[37], l[19], l[38], l[3]]))

k.append(sh.occ.addCurveLoop([l[0], l[1], l[2], l[37], l[18], l[17], l[16], l[36]]))
k.append(sh.occ.addCurveLoop([l[4], l[5], l[6], l[39], l[22], l[21], l[20], l[38]]))

r.append(sh.occ.addCurveLoop([l[29], l[30], l[31], l[28]]))
r.append(sh.occ.addCurveLoop([l[16], l[17], l[18], l[41], l[32], l[40]]))
r.append(sh.occ.addCurveLoop([l[20], l[21], l[22], l[43], l[34], l[42]]))
r.append(sh.occ.addCurveLoop([l[23], l[40], l[35], l[43]]))
r.append(sh.occ.addCurveLoop([l[19], l[42], l[33], l[41]]))

s = list()
q = list()

for a in k: s.append(sh.occ.addPlaneSurface([a]))
for a in r: q.append(sh.occ.addPlaneSurface([a]))
sh.occ.synchronize()

# # Volumes list

h = sh.occ.addSurfaceLoop(s)
v = sh.occ.addVolume([h])
sh.occ.synchronize()

# Physical surface

sh.addPhysicalGroup(3, [v], name='Fluid')
sh.addPhysicalGroup(2, s[4:8], name='FreeSurface')
sh.addPhysicalGroup(2, s[8:12]+r[:1], name='FSInterface')
sh.addPhysicalGroup(2, s[:4]+s[12:]+r[1:], name='Container')

# Write the mesh

sh.mesh.generate(3)
gmsh.write(f'{os.path.dirname(__file__)}/geometry_F.msh')
gmsh.fltk.run()
gmsh.finalize()