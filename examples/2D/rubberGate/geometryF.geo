Include "../../toolbox_2D.geo";
SetFactory("OpenCASCADE");

H = 0.079;
S = 0.005;
D = 0.14;
L = 0.1;

d = 1e-3;
eps = 1e-5;
N = 79;

// Point List

p = newp; Point(p) = {0,0,0,d};
p = newp; Point(p) = {L,0,0,d};
p = newp; Point(p) = {2*L+S,0,0,d};
p = newp; Point(p) = {0,D,0,d};
p = newp; Point(p) = {L,D,0,d};
p = newp; Point(p) = {L,H,0,d};
p = newp; Point(p) = {L,eps,0,d};

// Line List

c = newl; Line(c) = {1,2};
c = newl; Line(c) = {2,3};
c = newl; Line(c) = {4,1};
c = newl; Line(c) = {6,7};
c = newl; Line(c) = {5,6};
c = newl; Line(c) = {5,4};
c = newl; Line(c) = {2,7};

// Fluid Mesh

k = newcl; Curve Loop(k) = {1,7,4,5,6,3};
s = news; Plane Surface(s) = {k};
Transfinite Line{4} = N;

// Boundary Domains

Physical Surface("Fluid") = {s};
Physical Curve("FreeSurface") = {6};
Physical Curve("FSInterface") = {4};
Physical Curve("Reservoir") = {1:3,5};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {1:7};

Field[2] = MathEval;
Field[2].F = Sprintf("%g+F1*0.2",d);
Background Field = 2;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.Binary = 1;
Mesh 2;