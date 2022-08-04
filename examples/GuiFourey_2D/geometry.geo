// Parameters

f = 2;
d = 0.005;
N = 12;

L = 1;
HF = 2;
HS = 0.05;

// Points List

Point(1) = {0,0,0,d};
Point(2) = {L,0,0,d};
Point(3) = {L,HS,0,d};
Point(4) = {0,HS,0,d};
Point(5) = {L,HS+HF,0,d};
Point(6) = {0,HS+HF,0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};
Line(5) = {3,5};
Line(6) = {5,6};
Line(7) = {6,4};

// Solid Surface

Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};
Physical Surface("Solid") = {1};

Transfinite Line{2} = N;
Transfinite Line{4} = N;

Transfinite Surface{1};
Recombine Surface{1};

// Fluid Surface

Curve Loop(2) = {-3,5,6,7};
Plane Surface(2) = {2};
Physical Surface("Fluid") = {2};

// Boundaries

Physical Curve("FSInterface") = {3};
Physical Curve("FreeSurface") = {6};
Physical Curve("Clamped") = {2,4};
Physical Curve("Bottom") = {1};
Physical Curve("Wall") = {5,7};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {3};

Field[2] = MathEval;
Field[2].F = Sprintf("%g*F1*%g/(%g/2)+%g",f,d,L,d);

Field[3] = Box;
Field[3].VIn = d;
Field[3].VOut = 1;
Field[3].XMin = 0;
Field[3].XMax = L;
Field[3].YMin = 0;
Field[3].YMax = HS;

// Makes the Mesh

Field[4] = Min;
Field[4].FieldsList = {2,3};
Background Field = 4;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Algorithm = 5;
Mesh 2;
