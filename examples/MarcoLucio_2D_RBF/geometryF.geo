L = 0.146;
w = 0.012;
h = 0.08;
d = 0.005;

N = 16;
M = 4;

// Points List

Point(1) = {0,0,0,d};
Point(2) = {4*L,0,0,d};
Point(3) = {4*L,4*L,0,d};
Point(4) = {0,3*L,0,d};
Point(5) = {L,0,0,d};
Point(6) = {L,2*L,0,d};
Point(7) = {0,2*L,0,d};
Point(8) = {2*L,0,0,d};
Point(9) = {2*L,h,0,d};
Point(10) = {2*L+w,h,0,d};
Point(11) = {2*L+w,0,0,d};

// Lines List

Line(1) = {4,7};
Line(2) = {7,1};
Line(3) = {1,5};
Line(4) = {5,6};
Line(5) = {6,7};
Line(6) = {5,8};
Line(7) = {8,9};
Line(8) = {9,10};
Line(9) = {10,11};
Line(10) = {11,2};
Line(11) = {2,3};
Line(12) = {8,11};

// Fluid Surface

Curve Loop(1) = {2,3,4,5};
Plane Surface(1) = {1};
Physical Surface("Fluid") = {1};

Transfinite Line{7} = N;
Transfinite Line{8} = M;
Transfinite Line{9} = N;
Transfinite Line{12} = M;

// Physical Boundaries

Physical Curve("FSInterface") = {7,8,9};
Physical Curve("Reservoir") = {1,2,3,6,10,11};
Physical Curve("Polytope") = {7,8,9,12};
Physical Curve("FreeSurface") = {5,4};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {1,2,3,4,5,6,7,8,9,10,11,12};

Field[2] = MathEval;
Field[2].F = Sprintf("%g+F1*0.1",d);

Field[3] = Box;
Field[3].VIn = 1;
Field[3].VOut = d;
Field[3].XMin = 0;
Field[3].XMax = L;
Field[3].YMin = 0;
Field[3].YMax = 2*L;

// Makes the Mesh

Field[4] = Min;
Field[4].FieldsList = {2,3};
Background Field = 4;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Algorithm = 5;
Mesh 2;