L = 0.9;
HF = 0.25;
HS = 0.03;
R = 0.025;
C = 0.2;

d = 0.005;
N = 180;
M = 50;
P = 32;

// Points List

Point(1) = {L,0,0,d};
Point(2) = {0,0,0,d};
Point(3) = {L,HF,0,d};
Point(4) = {0,HF,0,d};
Point(5) = {0,HF+HS+R,0,d};
Point(6) = {L,HF+HS+R,0,d};

Point(7) = {C,HF+HS,0,d};
Point(8) = {C,HF+HS+R,0,d};
Point(9) = {C,HF+HS-R,0,d};

Point(10) = {L/2,HF+HS,0,d};
Point(11) = {L/2,HF+HS+R,0,d};
Point(12) = {L/2,HF+HS-R,0,d};

Point(13) = {L-C,HF+HS,0,d};
Point(14) = {L-C,HF+HS+R,0,d};
Point(15) = {L-C,HF+HS-R,0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {1,3};
Line(3) = {3,4};
Line(4) = {4,2};
Line(5) = {4,5};
Line(6) = {3,6};

Circle(7) = {8,7,9};
Circle(8) = {9,7,8};

Circle(9) = {11,10,12};
Circle(10) = {12,10,11};

Circle(11) = {14,13,15};
Circle(12) = {15,13,14};

// Fluid Surface

Curve Loop(1) = {-1,2,3,4};
Plane Surface(1) = {1};

// Transfinite Line{1} = N;
Transfinite Line{3} = N;
// Transfinite Line{2} = M;
// Transfinite Line{4} = M;


Transfinite Line{7:12} = P;

// Boundaries

Physical Surface("Fluid") = {1};

Physical Curve("Poly_1") = {7,8};
Physical Curve("Poly_2") = {9,10};
Physical Curve("Poly_3") = {11,12};
Physical Curve("Wall") = {1,2,4,5,6};

Physical Curve("FreeSurface") = {3};
Physical Curve("FSInterface") = {7,8,9,10,11,12};

// Makes the Mesh

Field[1] = MathEval;
Field[1].F = "Max(0.1*(0.25-y),0.005)";
Background Field = 1;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Algorithm = 5;
Mesh.Binary = 1;
Mesh 2;