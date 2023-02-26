Include "../../toolbox_3D.geo";
SetFactory("OpenCASCADE");

D = 1.1;
d = 0.01;
y = 0;

// Make the Solid

L = 0.03;
H = 0.3;
W = 0.1;

z = H/2;
x = L/2+0.6;
Call Hole_Square;

// Make the Fluid

L = 0.3;
H = 0.4;
W = 0.3;

z = H/2;
x = L/2;
Call Tri_Square;

// New Structure Part

p = newp; Point(p) = {D,-W/2,0,d};
p = newp; Point(p) = {D,W/2,0,d};
p = newp; Point(p) = {D,-W/2,H,d};
p = newp; Point(p) = {D,W/2,H,d};

l = newl; Line(l) = {14,17};
l = newl; Line(l) = {16,18};
l = newl; Line(l) = {13,19};
l = newl; Line(l) = {15,20};
l = newl; Line(l) = {17,18};
l = newl; Line(l) = {19,20};
l = newl; Line(l) = {17,19};
l = newl; Line(l) = {18,20};

k1 = newcl; Curve Loop(k1) = {17,25,31,27};
k2 = newcl; Curve Loop(k2) = {19,26,32,28};
k3 = newcl; Curve Loop(k3) = {29,32,30,31};
k4 = newcl; Curve Loop(k4) = {25,29,26,20};

s = news; Plane Surface(s) = {k1};
s = news; Plane Surface(s) = {k2};
s = news; Plane Surface(s) = {k3};
s = news; Plane Surface(s) = {k4,-5};

// Physical Surface

Physical Volume("Fluid") = {13};
Physical Surface("Polytope") = {1:6};
Physical Surface("FreeSurface") = {8,12};
Physical Surface("FSInterface") = {1:4,6};
Physical Surface("Reservoir") = {5,7,9:11,37:40};

// Makes the Mesh

Field[1] = MathEval;
Field[1].F = "Max(0.4*(0.3-x),0.01)";
Field[2] = MathEval;
Field[2].F = "Max(0.4*x,0.01)";
Field[3] = MathEval;
Field[3].F = "Max(0.4*(0.15-Fabs(y)),0.01)";
Field[4] = MathEval;
Field[4].F = "Max(0.4*(0.4-z),0.01)";
Field[5] = MathEval;
Field[5].F = "Max(0.4*z,0.01)";

Field[6] = Min;
Field[6].FieldsList = {1:5};
Background Field = 6;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Binary = 1;
Mesh 3;