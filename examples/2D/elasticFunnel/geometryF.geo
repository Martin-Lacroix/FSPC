R = 2.25;
H = 3.75;
B = 4.87;
h = 2.5;
b = 1.3;

d = 0.05;
N = 160;
M = 80;

// Points List

Point(1) = {-B/2,H+h,0,d};
Point(2) = {-b/2,H,0,d};
Point(3) = {-R,H,0,d};
Point(5) = {-R,0,0,d};
Point(7) = {B/2,H+h,0,d};
Point(8) = {b/2,H,0,d};
Point(9) = {R,H,0,d};
Point(10) = {R,0,0,d};
Point(11) = {0,0,0,d};

// Lines List

Line(1) = {5,3};
Line(2) = {9,10};
Circle(3) = {5,11,10};
Line(4) = {1,2};
Line(5) = {2,8};
Line(6) = {8,7};
Line(7) = {7,1};

// Fluid Surface

Curve Loop(1) = {4,5,6,7};
Plane Surface(1) = {1};

Transfinite Line{1} = M;
Transfinite Line{2} = M;
Transfinite Line{3} = N;

// Physical Boundaries

Physical Surface("Fluid") = {1};
Physical Curve("FSInterface") = {1,2,3};
Physical Curve("Reservoir") = {4,6};
Physical Curve("FreeSurface") = {5,7};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {1,2,3,4,5,6,7};

Field[2] = MathEval;
Field[2].F = Sprintf("%g+F1*0.1",d);

// Makes the Mesh

Field[3] = Min;
Field[3].FieldsList = {2};
Background Field = 3;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Algorithm = 5;
Mesh 2;