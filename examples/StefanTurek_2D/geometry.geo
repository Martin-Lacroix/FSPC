f = 0;
d = 0.01;
Nx = 40;
Ny = 4;

L = 2.5;
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
Line(10) = {7,8};

// Solid Mesh

Curve Loop(1) = {6,-10,-5};
Plane Surface(1) = {1};
Recombine Surface{1};

Transfinite Line{7} = Nx;
Transfinite Line{8} = Ny;
Transfinite Line{9} = Nx;
Transfinite Line{10} = Ny;

Curve Loop(2) = {-9,-8,-7,10};
Plane Surface(2) = {2};
Transfinite Surface{2};
Recombine Surface{2};

Physical Surface("Solid") = {1,2};

// Fluid Mesh

Curve Loop(3) = {1,2,3,4};
Plane Surface(3) = {3,-1,-2};
Physical Surface("Fluid") = {3};

// Boundary Domains

Physical Curve("FSInterface") = {6,-9,-8,-7,-5};
Physical Curve("Border") = {1,3};
Physical Curve("Inlet") = {4};
Physical Curve("FreeSurface") = {2};
Physical Curve("Clamped") = {5,6};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {5,6,7,8,9};

Field[2] = MathEval;
Field[2].F = Sprintf("%g*F1*%g/(%g/2)+%g",f,d,L,d);

// Makes the Mesh

Field[4] = Min;
Field[4].FieldsList = {2};
Background Field = 4;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Algorithm = 5;
Mesh 2;
