Include "../../toolbox_2D.geo";
SetFactory("OpenCASCADE");

d = 0.005;

// Make the Solid

y = 0.04;
H = 0.08;
x = 0.298;
L = 0.012;
Call Hole_Square;

// Make the Fluid

x = 0.073;
L = 0.146;
H = 0.292;
y = 0.146;
Call Tri_Square;

// New Structure Part

p = newp; Point(p) = {0,3*L,0,d};
p = newp; Point(p) = {4*L,0,0,d};
p = newp; Point(p) = {4*L,4*L,0,d};

c = newl; Line(c) = {8,9};
c = newl; Line(c) = {6,1};
c = newl; Line(c) = {2,10};
c = newl; Line(c) = {10,11};

// Physical Boundary

Physical Surface("Fluid") = {11};
Physical Curve("FSInterface") = {2:4};
Physical Curve("Reservoir") = {1,6,9,12:15};
Physical Curve("FreeSurface") = {7,8};
Physical Curve("Polytope") = {1:4};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {1:15};

Field[2] = MathEval;
Field[2].F = Sprintf("%g+F1*0.1",d);
Background Field = 2;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.Binary = 1;
Mesh 2;