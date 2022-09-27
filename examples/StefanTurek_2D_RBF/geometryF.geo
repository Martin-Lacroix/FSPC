d = 0.03;

L = 1.5; // 2.5
X = 0.2;
Y = 0.2;
R = 0.05;
H = 0.41;
Ls = 0.35;
A = Asin(0.2);

// Points List

Point(1) = {0,0,0,d};
Point(2) = {L,0,0,d};
Point(3) = {L,H,0,d};
Point(4) = {0,H,0,d};

Point(5) = {X,Y,0,d};
Point(6) = {X-R,Y,0,d};

Point(7) = {X+R*Cos(A),Y+R*Sin(A),0,d};
Point(8) = {X+R*Cos(A),Y-R*Sin(A),0,d};
Point(9) = {X+R+Ls,Y+R*Sin(A),0,d};
Point(10) = {X+R+Ls,Y-R*Sin(A),0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Circle(5) = {6,5,7};
Circle(6) = {6,5,8};

Line(7) = {7,9};
Line(8) = {9,10};
Line(9) = {10,8};

// Fluid Mesh

Curve Loop(1) = {1,2,3,4};
Curve Loop(2) = {-9,-8,-7,-5,6};

Plane Surface(1) = {1,-2};
Physical Surface("Fluid") = {1};

// Boundary Domains

Physical Curve("FSInterface") = {7,8,9};
Physical Curve("Border") = {1,3};
Physical Curve("Inlet") = {4};
Physical Curve("Outlet") = {2};
Physical Curve("Polytope") = {5,6,7,8,9};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {4,5,6,7,8,9};

Field[2] = MathEval;
Field[2].F = Sprintf("%g+F1*0.05",d);

// Makes the Mesh

Field[3] = Min;
Field[3].FieldsList = {2};
Background Field = 3;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Algorithm = 5;
Mesh 2;
