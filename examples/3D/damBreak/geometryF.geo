Lx = 1.1;
Ly = 0.3;
Lz = 0.4;

S = 0.6;
Sx = 0.03;
Sy = 0.1;
Sz = 0.2;

Fx = 0.3;

d = 0.01;
N = 20;
M = 10;
P = 4;

// Points List

Point(1) = {0,0,0,d};
Point(2) = {Fx,0,0,d};
Point(3) = {Lx,0,0,d};
Point(4) = {Lx,0,Lz,d};
Point(5) = {Fx,0,Lz,d};
Point(6) = {0,0,Lz,d};

Point(7) = {0,Ly,0,d};
Point(8) = {Fx,Ly,0,d};
Point(9) = {Lx,Ly,0,d};
Point(10) = {Lx,Ly,Lz,d};
Point(11) = {Fx,Ly,Lz,d};
Point(12) = {0,Ly,Lz,d};

Point(13) = {S,(Ly-Sy)/2,0,d};
Point(14) = {S+Sx,(Ly-Sy)/2,0,d};
Point(15) = {S+Sx,(Ly+Sy)/2,0,d};
Point(16) = {S,(Ly+Sy)/2,0,d};

Point(17) = {S,(Ly-Sy)/2,Sz,d};
Point(18) = {S+Sx,(Ly-Sy)/2,Sz,d};
Point(19) = {S+Sx,(Ly+Sy)/2,Sz,d};
Point(20) = {S,(Ly+Sy)/2,Sz,d};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(5) = {4,5};
Line(6) = {5,6};
Line(7) = {6,1};

Line(8) = {7,8};
Line(9) = {8,9};
Line(10) = {9,10};
Line(11) = {10,11};
Line(12) = {11,12};
Line(13) = {12,7};

Line(14) = {1,7};
Line(15) = {2,8};
Line(16) = {3,9};
Line(17) = {4,10};
Line(18) = {5,11};
Line(19) = {6,12};

Line(20) = {2,5};
Line(21) = {8,11};

Line(22) = {13,14};
Line(23) = {14,15};
Line(24) = {15,16};
Line(25) = {16,13};

Line(26) = {17,18};
Line(27) = {18,19};
Line(28) = {19,20};
Line(29) = {20,17};

Line(30) = {13,17};
Line(31) = {14,18};
Line(32) = {15,19};
Line(33) = {16,20};

// Surface List

Curve Loop(1) = {7,14,-13,-19};
Curve Loop(2) = {-20,15,21,-18};
Curve Loop(3) = {1,20,6,7};
Curve Loop(4) = {8,21,12,13};
Curve Loop(5) = {1,15,-8,-14};
Curve Loop(6) = {-6,18,12,-19};

Curve Loop(7) = {-25,-24,-23,-22};
Curve Loop(8) = {26,27,28,29};
Curve Loop(9) = {22,31,-26,-30};
Curve Loop(10) = {33,-28,-32,24};
Curve Loop(11) = {23,32,-27,-31};
Curve Loop(12) = {30,-29,-33,25};

Curve Loop(13) = {2,16,-9,-15};
Curve Loop(14) = {-5,17,11,-18};
Curve Loop(15) = {2,3,5,-20};
Curve Loop(16) = {9,10,11,-21};
Curve Loop(17) = {16,10,-17,-3};

Plane Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};
Plane Surface(5) = {5};
Plane Surface(6) = {6};

Plane Surface(7) = {7};
Plane Surface(8) = {8};
Plane Surface(9) = {9};
Plane Surface(10) = {10};
Plane Surface(11) = {11};
Plane Surface(12) = {12};

Plane Surface(13) = {13,-7};
Plane Surface(15) = {15};
Plane Surface(16) = {16};
Plane Surface(17) = {17};

// Mesh of the Fluid

Surface Loop(1) = {1,2,3,4,5,6};
Volume(1) = {1};

Transfinite Line{30} = N;
Transfinite Line{31} = N;
Transfinite Line{32} = N;
Transfinite Line{33} = N;

Transfinite Line{23} = M;
Transfinite Line{25} = M;
Transfinite Line{27} = M;
Transfinite Line{29} = M;

Transfinite Line{22} = P;
Transfinite Line{24} = P;
Transfinite Line{26} = P;
Transfinite Line{28} = P;

// Physical Surfaces

Physical Volume("Fluid") = {1};
Physical Surface("FreeSurface") = {2,6};
Physical Surface("FSInterface") = {8,9,10,11,12};
Physical Surface("Reservoir") = {1,3,4,5,7,13,15,16,17};
Physical Surface("Polytope") = {7,8,9,10,11,12};

// Distance from X

Field[1] = MathEval;
Field[1].F = "Max(0.4*(0.3-x),0.01)";
Field[2] = MathEval;
Field[2].F = "Max(0.4*x,0.01)";

// Distance from Y

Field[3] = MathEval;
Field[3].F = "Max(0.4*(0.3-y),0.01)";
Field[4] = MathEval;
Field[4].F = "Max(0.4*y,0.01)";

// Distance from Z

Field[5] = MathEval;
Field[5].F = "Max(0.4*(0.4-z),0.01)";
Field[6] = MathEval;
Field[6].F = "Max(0.4*z,0.01)";

// Solid Mesh Box

Field[7] = Box;
Field[7].VIn = d;
Field[7].VOut = 1;
Field[7].XMin = S;
Field[7].XMax = S+Sx;
Field[7].YMin = (Ly-Sy)/2;
Field[7].YMax = (Ly+Sy)/2;
Field[7].ZMin = 0;
Field[7].ZMax = Sz;

// Makes the Mesh

Field[8] = Min;
Field[8].FieldsList = {1,2,3,4,5,6,7};
Background Field = 8;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Algorithm = 5;
Mesh 3;