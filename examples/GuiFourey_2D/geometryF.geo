// Parameters

d = 0.005;
M = 200;

L = 1;
HF = 2;
HS = 0.05;

// Points List

Point(1) = {L,HS,0,d};
Point(2) = {0,HS,0,d};
Point(3) = {L,HS+HF,0,d};
Point(4) = {0,HS+HF,0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {1,3};
Line(3) = {3,4};
Line(4) = {4,2};

// Fluid Surface

Curve Loop(1) = {-1,2,3,4};
Plane Surface(1) = {1};
Physical Surface("Fluid") = {1};

Transfinite Line{1} = M;

// Boundaries

Physical Curve("FSInterface") = {1};
Physical Curve("FreeSurface") = {3};
Physical Curve("Wall") = {2,4};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {1};

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