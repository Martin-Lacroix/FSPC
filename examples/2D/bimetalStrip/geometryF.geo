H = 0.1;
L1 = 0.2;
L2 = 0.5;
L3 = 0.1;
S = 0.001;

d = 1e-3;
N = 80;
M = 3;

// Points List

Point(1) = {-L1,-H/2,0,d};
Point(2) = {L2,-H/2,0,d};
Point(3) = {L2,H/2,0,d};
Point(4) = {-L1,H/2,0,d};

Point(5) = {0,-S,0,d};
Point(6) = {L3,-S,0,d};
Point(7) = {L3,S,0,d};
Point(8) = {0,S,0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Line(5) = {5,6};
Line(6) = {6,7};
Line(7) = {7,8};
Line(8) = {8,5};

// Fluid Mesh

Curve Loop(1) = {1,2,3,4};
Curve Loop(2) = {5,6,7,8};
Plane Surface(1) = {1,-2};

Transfinite Line{5} = N;
Transfinite Line{6} = M;
Transfinite Line{7} = N;
Transfinite Line{8} = M;

// Boundary Domains

Physical Surface("Fluid") = {1};
Physical Curve("FSInterface") = {5,6,7,8};
Physical Curve("Border") = {1,3};
Physical Curve("Outlet") = {2};
Physical Curve("Inlet") = {4};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {5,6,7,8};

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
Mesh.Binary = 1;
Mesh 2;
