L = 5;
R = 2;

d = 0.1;
N = 51;

// Points List

Point(1) = {-L,-L,0,d};
Point(2) = {L,-L,0,d};
Point(3) = {L,L,0,d};
Point(4) = {-L,L,0,d};

Point(5) = {-R,-R,0,d};
Point(6) = {R,-R,0,d};
Point(7) = {R,R,0,d};
Point(8) = {-R,R,0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Line(5) = {5,6};
Line(6) = {6,7};
Line(7) = {7,8};
Line(8) = {8,5};

// Fluid Surface

Curve Loop(1) = {1,2,3,4};
Curve Loop(2) = {5,6,7,8};
Plane Surface(1) = {1,-2};
Transfinite Line{5:8} = N;

// Boundaries

Physical Surface("Fluid") = {1};
Physical Curve("FSInterface") = {5,6,7,8};
Physical Curve("Wall") = {1,2,3,4};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {5,6,7,8};

Field[2] = MathEval;
Field[2].F = Sprintf("%g+F1*0.05",d);
Background Field = 2;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Algorithm = 5;
Mesh.Binary = 1;
Mesh 2;