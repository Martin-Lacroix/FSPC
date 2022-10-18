H = 0.12;
B = 0.14;
A = 0.055;
L = 0.04;
w = 6e-4;
s = 0.01;

d = 1e-3;
NS = 40;
MS = 2;

NF = 50;
MF1 = 30;
MF2 = 20;

// Points List

Point(1) = {0,0,0,d};
Point(2) = {A+B,0,0,d};
Point(3) = {A+B,H,0,d};
Point(4) = {0,H,0,d};

Point(5) = {A-s/2,(H-s)/2,0,d};
Point(6) = {A+s/2,(H-s)/2,0,d};
Point(7) = {A+s/2,(H+s)/2,0,d};
Point(8) = {A-s/2,(H+s)/2,0,d};

Point(9) = {A+s/2,(H-w)/2,0,d};
Point(10) = {A+s/2+L,(H-w)/2,0,d};
Point(11) = {A+s/2+L,(H+w)/2,0,d};
Point(12) = {A+s/2,(H+w)/2,0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Line(7) = {5,6};
Line(8) = {6,9};
Line(9) = {9,10};
Line(10) = {10,11};
Line(11) = {11,12};
Line(12) = {12,7};
Line(13) = {7,8};
Line(14) = {8,5};

// Fluid Mesh

Curve Loop(1) = {1,2,3,4};
Curve Loop(2) = {7,8,9,10,11,12,13,14};

Plane Surface(1) = {1,-2};
Physical Surface("Fluid") = {1};

Transfinite Line{9} = NS;
Transfinite Line{10} = MS;
Transfinite Line{11} = NS;

Transfinite Line{1} = NF;
Transfinite Line{2} = MF2;
Transfinite Line{3} = NF;
Transfinite Line{4} = MF1;

// Boundary Domains

Physical Curve("Polytope") = {7,8,9,10,11,12,13,14};
Physical Curve("FSInterface") = {9,10,11};
Physical Curve("FreeSurface") = {2};
Physical Curve("Border") = {1,3};
Physical Curve("Inlet") = {4};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {7,8,9,10,11,12,13,14};

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
