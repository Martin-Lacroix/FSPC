H = 0.079;
S = 0.005;
D = 0.14;
L1 = 0.1;
L2 = 0.1;

d = 1e-3;
eps = 1e-5;
N = 79;

// Point List

Point(1) = {0,0,0,d};
Point(2) = {L1,0,0,d};
Point(3) = {L1+S+L2,0,0,d};
Point(4) = {0,D,0,d};
Point(5) = {L1,D,0,d};
Point(6) = {L1,H,0,d};
Point(7) = {L1,eps,0,d};

// Line List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {4,1};
Line(4) = {6,7};
Line(5) = {5,6};
Line(6) = {5,4};
Line(7) = {2,7};

// Fluid Mesh

Curve Loop(1) = {1,7,-4,-5,6,3};
Plane Surface(1) = {1};

Transfinite Line{4} = N;

// Boundary Domains

Physical Surface("Fluid") = {1};
Physical Curve("FreeSurface") = {6};
Physical Curve("FSInterface") = {4};
Physical Curve("Reservoir") = {1,2,3,5};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {1,2,3,4,5,6,7};

Field[2] = MathEval;
Field[2].F = Sprintf("%g+F1*0.2",d);

Field[3] = Box;
Field[3].VIn = 1;
Field[3].VOut = d;
Field[3].XMin = 0;
Field[3].XMax = L1;
Field[3].YMin = 0;
Field[3].YMax = D;

// Makes the Mesh

Field[4] = Min;
Field[4].FieldsList = {2,3};
Background Field = 4;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Algorithm = 5;
Mesh.Binary = 1;
Mesh 2;