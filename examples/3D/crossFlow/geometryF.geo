H = 0.4;
B = 0.25;
L1 = 0.15;
L2 = 0.2;

b = 0.02;
h = 0.1;
w = 0.005;

d = 2e-3;
N = 40;
M = 10;
P = 4;

// Point List

Point(1) = {0,0,0,d};
Point(2) = {L1+L2,0,0,d};
Point(3) = {L1+L2,B,0,d};
Point(4) = {0,B,0,d};
Point(5) = {0,0,H,d};
Point(6) = {L1+L2,0,H,d};
Point(7) = {L1+L2,B,H,d};
Point(8) = {0,B,H,d};

Point(9) = {L1,(B-b)/2,0,d};
Point(10) = {L1+w,(B-b)/2,0,d};
Point(11) = {L1+w,(B+b)/2,0,d};
Point(12) = {L1,(B+b)/2,0,d};
Point(13) = {L1,(B-b)/2,h,d};
Point(14) = {L1+w,(B-b)/2,h,d};
Point(15) = {L1+w,(B+b)/2,h,d};
Point(16) = {L1,(B+b)/2,h,d};

// Line List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};
Line(5) = {5,6};
Line(6) = {6,7};
Line(7) = {7,8};
Line(8) = {8,5};

Line(9) = {9,10};
Line(10) = {10,11};
Line(11) = {11,12};
Line(12) = {12,9};
Line(13) = {13,14};
Line(14) = {14,15};
Line(15) = {15,16};
Line(16) = {16,13};

Line(17) = {1,5};
Line(18) = {2,6};
Line(19) = {3,7};
Line(20) = {4,8};

Line(21) = {9,13};
Line(22) = {10,14};
Line(23) = {11,15};
Line(24) = {12,16};

// FS Interface

Curve Loop(1) = {-12,-11,-10,-9};
Curve Loop(2) = {13,14,15,16};
Curve Loop(3) = {9,22,-13,-21};
Curve Loop(4) = {11,24,-15,-23};
Curve Loop(5) = {10,23,-14,-22};
Curve Loop(6) = {12,21,-16,-24};

Plane Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};
Plane Surface(5) = {5};
Plane Surface(6) = {6};

Transfinite Line{21} = N;
Transfinite Line{22} = N;
Transfinite Line{23} = N;
Transfinite Line{24} = N;

Transfinite Line{10} = M;
Transfinite Line{12} = M;
Transfinite Line{14} = M;
Transfinite Line{16} = M;

Transfinite Line{9} = P;
Transfinite Line{11} = P;
Transfinite Line{13} = P;
Transfinite Line{15} = P;

// Mesh of the Fluid

Curve Loop(7) = {-4,-3,-2,-1};
Curve Loop(8) = {5,6,7,8};
Curve Loop(9) = {1,18,-5,-17};
Curve Loop(10) = {3,20,-7,-19};
Curve Loop(11) = {2,19,-6,-18};
Curve Loop(12) = {4,17,-8,-20};

Plane Surface(7) = {7,-1};
Plane Surface(8) = {8};
Plane Surface(9) = {9};
Plane Surface(10) = {10};
Plane Surface(11) = {11};
Plane Surface(12) = {12};

Surface Loop(1) = {2,3,4,5,6,7,8,9,10,11,12};
Volume(1) = {1};

// Physical Surfaces

Physical Surface("Bottom") = {1,7};
Physical Surface("Polytope") = {1,2,3,4,5,6};
Physical Surface("FSInterface") = {2,3,4,5,6};
Physical Surface("Reservoir") = {8,9,10};
Physical Surface("Outlet") = {11};
Physical Surface("Inlet") = {12};
Physical Volume("Fluid") = {1};

// Distance from X

Field[1] = MathEval;
Field[1].F = "Max(0.002 + 0.1*(x-0.155),0)";
Field[2] = MathEval;
Field[2].F = "Max(0.002 + 0.1*(0.15-x),0)";

// Distance from Y

Field[3] = MathEval;
Field[3].F = "Max(0.002 + 0.1*(y-0.135),0)";
Field[4] = MathEval;
Field[4].F = "Max(0.002 + 0.1*(0.115-y),0)";

// Distance from Z

Field[5] = MathEval;
Field[5].F = "Max(0.002 + 0.1*(z-0.1),0)";

// Makes the Mesh

Field[6] = Max;
Field[6].FieldsList = {1,2,3,4,5};
Background Field = 6;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Algorithm = 5;
Mesh 3;
