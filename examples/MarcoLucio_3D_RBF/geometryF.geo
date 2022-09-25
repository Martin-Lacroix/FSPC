L = 0.146;
w = 0.012;
h = 0.08;
D = 0.2;

d = 0.006;
eps = 1e-5;

// Points List

Point(1) = {0,0,0,d};
Point(2) = {L,0,0,d};
Point(3) = {2*L,0,0,d};
Point(4) = {2*L+w,0,0,d};
Point(5) = {4*L,0,0,d};

Point(6) = {0,D,0,d};
Point(7) = {L,D,0,d};
Point(8) = {2*L,D,0,d};
Point(9) = {2*L+w,D,0,d};
Point(10) = {4*L,D,0,d};

Point(11) = {0,0,3*L,d};
Point(12) = {4*L,0,3*L,d};
Point(13) = {0,D,3*L,d};
Point(14) = {4*L,D,3*L,d};

Point(15) = {0,0,2*L,d};
Point(16) = {L,0,2*L,d};
Point(17) = {0,D,2*L,d};
Point(18) = {L,D,2*L,d};

Point(19) = {2*L,eps,h,d};
Point(20) = {2*L+w,eps,h,d};
Point(21) = {2*L,D-eps,h,d};
Point(22) = {2*L+w,D-eps,h,d};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,5};
Line(5) = {6,7};
Line(6) = {7,8};
Line(7) = {8,9};
Line(8) = {9,10};

Line(9) = {11,12};
Line(10) = {13,14};

Line(11) = {1,6};
Line(12) = {2,7};
Line(13) = {16,18};
Line(14) = {15,17};
Line(15) = {15,16};
Line(16) = {17,18};
Line(17) = {1,15};
Line(18) = {2,16};
Line(19) = {7,18};
Line(20) = {6,17};

Line(21) = {15,11};
Line(22) = {17,13};
Line(23) = {11,13};
Line(24) = {12,14};
Line(25) = {5,10};
Line(26) = {5,12};
Line(27) = {10,14};

Line(28) = {4,9};
Line(29) = {3,8};
Line(30) = {3,19};
Line(31) = {4,20};
Line(32) = {8,21};
Line(33) = {9,22};
Line(34) = {19,20};
Line(35) = {21,22};
Line(36) = {19,21};
Line(37) = {20,22};

// Mesh of the Fluid

Curve Loop(1) = {1,12,-5,-11};
Curve Loop(2) = {15,13,-16,-14};
Curve Loop(3) = {11,20,-14,-17};
Curve Loop(4) = {18,13,-19,-12};
Curve Loop(5) = {1,18,-15,-17};
Curve Loop(6) = {5,19,-16,-20};

Plane Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};
Plane Surface(5) = {5};
Plane Surface(6) = {6};

Surface Loop(1) = {1,2,3,4,5,6};
Volume(1) = {1};
Physical Volume("Fluid") = {1};

// Mesh of the Solid

Curve Loop(7) = {7,-28,-3,29};
Curve Loop(8) = {34,37,-35,-36};
Curve Loop(9) = {28,33,-37,-31};
Curve Loop(10) = {30,36,-32,-29};
Curve Loop(11) = {3,31,-34,-30};
Curve Loop(12) = {32,35,-33,-7};

Plane Surface(7) = {7};
Plane Surface(8) = {8};
Plane Surface(9) = {9};
Plane Surface(10) = {10};
Plane Surface(11) = {11};
Plane Surface(12) = {12};

// Reservoir Surface

Curve Loop(13) = {2,3,4,26,-9,-21,15,-18};
Curve Loop(14) = {6,7,8,27,-10,-22,16,-19};
Curve Loop(15) = {2,29,-6,-12};
Curve Loop(16) = {4,25,-8,-28};
Curve Loop(17) = {14,22,-23,-21};
Curve Loop(18) = {25,27,-24,-26};

Plane Surface(13) = {13};
Plane Surface(14) = {14};
Plane Surface(15) = {15};
Plane Surface(16) = {16};
Plane Surface(17) = {17};
Plane Surface(18) = {18};

// Physical Surfaces

Physical Surface("FreeSurface") = {2,4};
Physical Surface("FSInterface") = {7,8,9,10,11,12};
Physical Surface("Reservoir") = {1,3,5,6,7,13,14,15,16,17,18};

// Fluid Mesh Size

Field[1] = Box;
Field[1].VIn = 1;
Field[1].VOut = d;
Field[1].XMin = 0;
Field[1].XMax = L;
Field[1].YMin = 0;
Field[1].YMax = D;
Field[1].ZMin = 0;
Field[1].ZMax = 2*L;

// Distance from X

Field[2] = MathEval;
Field[2].F = "0.006+0.5*Fabs(x)";
Field[3] = MathEval;
Field[3].F = "0.006+0.5*Fabs(0.146-x)";

// Distance from Y

Field[4] = MathEval;
Field[4].F = "0.006+0.5*Fabs(y)";
Field[5] = MathEval;
Field[5].F = "0.006+0.5*Fabs(0.2-y)";

// Distance from Z

Field[6] = MathEval;
Field[6].F = "0.006+0.5*Fabs(z)";
Field[7] = MathEval;
Field[7].F = "0.006+0.5*Fabs(0.292-z)";

// Makes the Mesh

Field[8] = Min;
Field[8].FieldsList = {1,2,3,4,5,6,7};
Background Field = 8;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Algorithm = 5;
Mesh 3;