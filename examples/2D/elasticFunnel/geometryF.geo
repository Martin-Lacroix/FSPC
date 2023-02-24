Include "../../toolbox_2D.geo";

x = 0;
y = 5;
R = 2.25;
d = 0.05;
N = 160;

// New Structure Part

c = newc; Circle(c) = {0,0,0,R,Pi,0};
p = newp; Point(p) = {-R,3.75,0,d};
p = newp; Point(p) = {R,3.75,0,d};
l = newl; Line(l) = {3,1};
l = newl; Line(l) = {4,2};

Transfinite Line{c} = N;
Transfinite Line{2,3} = Ceil(N/2);

// Make the Trapez

L = 1.3;
H = 2.5;
W = 4.87;
Call Tri_Trapez;

// Physical Boundary

Physical Surface("Fluid") = {9};
Physical Curve("FSInterface") = {1:3};
Physical Curve("FreeSurface") = {4,6};
Physical Curve("Reservoir") = {5,7};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {1:7};

Field[2] = MathEval;
Field[2].F = Sprintf("%g+F1*0.1",d);
Background Field = 2;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh 2;