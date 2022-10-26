H = 0.079;
D = 0.14;
L1 = 0.1;
L2 = 0.1;
W = 0.1;

d = 0.003;
eps = 1e-3;
hps = 1e-5;

N = 30;
M = 35;

// Point List

Point(1) = {0,0,0,d};
Point(2) = {L1,0,0,d};
Point(3) = {L1+L2,0,0,d};
Point(4) = {0,W,0,d};
Point(5) = {L1,W,0,d};
Point(6) = {L1+L2,W,0,d};
Point(7) = {0,0,D,d};
Point(8) = {L1,eps,D,d};
Point(9) = {L1+L2,0,D,d};
Point(10) = {0,W,D,d};
Point(11) = {L1,W-eps,D,d};
Point(12) = {L1+L2,W,D,d};
Point(13) = {L1,eps,H,d};
Point(14) = {L1,W-eps,H,d};
Point(15) = {L1,eps,hps,d};
Point(16) = {L1,W-eps,hps,d};
Point(17) = {L1,W,D,d};
Point(18) = {L1,0,D,d};
Point(19) = {L1,eps,0,d};
Point(20) = {L1,W-eps,0,d};

// Line List

Line(1) = {1,2};
Line(2) = {11,17};
Line(3) = {4,5};
Line(4) = {8,18};
Line(5) = {1,4};
Line(6) = {3,6};
Line(7) = {7,18};
Line(8) = {18,9};
Line(10) = {10,17};
Line(11) = {17,12};
Line(12) = {7,10};
Line(14) = {1,7};
Line(15) = {4,10};
Line(16) = {3,9};
Line(17) = {6,12};
Line(18) = {13,8};
Line(19) = {14,11};
Line(20) = {13,14};
Line(21) = {8,11};
Line(22) = {2,18};
Line(23) = {19,20};
Line(24) = {17,5};
Line(25) = {15,16};
Line(26) = {15,13};
Line(27) = {16,14};
Line(28) = {15,19};
Line(29) = {16,20};
Line(30) = {2,19};
Line(31) = {5,20};
Line(32) = {2,3};
Line(33) = {5,6};

// FS Interface

Curve Loop(1) = {26,20,-27,-25};
Curve Loop(2) = {-18,20,19,-21};
Curve Loop(3) = {4,-22,30,-28,26,18};
Curve Loop(4) = {-2,-19,-27,29,-31,-24};
Curve Loop(5) = {28,23,-29,-25};

Plane Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};
Plane Surface(5) = {5};

// Boundary Surface

Curve Loop(6) = {32,6,-33,31,-23,-30};
Curve Loop(7) = {33,17,-11,24};
Curve Loop(8) = {32,16,-8,-22};

Plane Surface(6) = {6};
Plane Surface(7) = {7};
Plane Surface(8) = {8};

// Mesh of the Fluid

Curve Loop(9) = {1,22,-7,-14};
Curve Loop(10) = {3,-24,-10,-15};
Curve Loop(11) = {5,15,-12,-14};
Curve Loop(12) = {1,30,23,-31,-3,-5};
Curve Loop(13) = {7,-4,21,2,-10,-12};

Plane Surface(9) = {9};
Plane Surface(10) = {10};
Plane Surface(11) = {11};
Plane Surface(12) = {12};
Plane Surface(13) = {13};

Transfinite Line{26} = N;
Transfinite Line{27} = N;

Transfinite Line{20} = M;
Transfinite Line{25} = M;

Surface Loop(1) = {1,2,3,4,5,9,10,11,12,13};
Volume(1) = {1};

// Physical Surfaces

Physical Surface("Reservoir") = {2,6,7,8,9,10,11,12};
Physical Surface("FreeSurface") = {13};
Physical Surface("FSInterface") = {1};
Physical Volume("Fluid") = {1};

// Fluid Mesh Size

Field[1] = Box;
Field[1].VIn = 1;
Field[1].VOut = d;
Field[1].XMin = 0;
Field[1].XMax = L1;
Field[1].YMin = 0;
Field[1].YMax = W;
Field[1].ZMin = 0;
Field[1].ZMax = D;

// Distance from X

Field[2] = MathEval;
Field[2].F = "0.003 + 0.3*Fabs(x)";
Field[3] = MathEval;
Field[3].F = "0.003 + 0.3*Fabs(0.1-x)";

// Distance from Y

Field[4] = MathEval;
Field[4].F = "0.003 + 0.3*Fabs(y)";
Field[5] = MathEval;
Field[5].F = "0.003 + 0.3*Fabs(0.1-y)";

// Distance from Z

Field[6] = MathEval;
Field[6].F = "0.003 + 0.3*Fabs(z)";
Field[7] = MathEval;
Field[7].F = "0.003 + 0.3*Fabs(0.14-z)";

// Makes the Mesh

Field[8] = Min;
Field[8].FieldsList = {1,2,3,4,5,6,7};
Background Field = 8;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Algorithm = 5;
Mesh 3;