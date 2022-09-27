H = 0.079;
S = 0.005;
D = 0.14;
L1 = 0.1;
L2 = 0.1;
W = 0.1;

eps = 1e-5;
d = 3e-3;

// Point List

Point(1) = {0,0,0,d};
Point(2) = {L1,0,0,d};
Point(3) = {L1+S+L2,0,0,d};
Point(4) = {0,W,0,d};
Point(5) = {L1,W,0,d};
Point(6) = {L1+S+L2,W,0,d};
Point(7) = {0,0,D,d};
Point(8) = {L1,0,D,d};
Point(9) = {L1+S,0,D,d};
Point(10) = {L1+S+L2,0,D,d};
Point(11) = {0,W,D,d};
Point(12) = {L1,W,D,d};
Point(13) = {L1+S,W,D,d};
Point(14) = {L1+S+L2,W,D,d};
Point(15) = {L1,0,H,d};
Point(16) = {L1+S,0,H,d};
Point(17) = {L1,W,H,d};
Point(18) = {L1+S,W,H,d};
Point(19) = {L1,eps,eps,d};
Point(20) = {L1+S,eps,eps,d};
Point(21) = {L1,W-eps,eps,d};
Point(22) = {L1+S,W-eps,eps,d};

// Line List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {4,5};
Line(4) = {5,6};
Line(5) = {1,4};
Line(6) = {3,6};
Line(7) = {7,8};
Line(8) = {8,9};
Line(9) = {9,10};
Line(10) = {11,12};
Line(11) = {12,13};
Line(12) = {13,14};
Line(13) = {7,11};
Line(14) = {1,7};
Line(15) = {4,11};
Line(16) = {3,10};
Line(17) = {6,14};
Line(18) = {15,8};
Line(19) = {16,9};
Line(20) = {17,12};
Line(21) = {18,13};
Line(22) = {15,16};
Line(23) = {17,18};
Line(24) = {16,18};
Line(25) = {15,17};
Line(26) = {8,12};
Line(27) = {9,13};
Line(28) = {2,5};
Line(29) = {2,15};
Line(30) = {5,17};

Line(31) = {19,20};
Line(32) = {21,22};
Line(33) = {20,22};
Line(34) = {19,21};
Line(35) = {19,15};
Line(36) = {20,16};
Line(37) = {22,18};
Line(38) = {21,17};

Line(39) = {2,19};
Line(40) = {5,21};

// Mesh of the Solid

Curve Loop(1) = {22,24,-23,-25};
Curve Loop(2) = {34,32,-33,-31};
Curve Loop(3) = {31,36,-22,-35};
Curve Loop(4) = {38,23,-37,-32};
Curve Loop(5) = {33,37,-24,-36};
Curve Loop(6) = {35,25,-38,-34};

Plane Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};
Plane Surface(5) = {5};
Plane Surface(6) = {6};

Transfinite Surface{1:6};
Recombine Surface{1:6};

Surface Loop(1) = {1,2,3,4,5,6};
Volume(1) = {1};
Physical Volume("Solid") = {1};

Transfinite Volume(1);
Recombine Volume(1);

// Polytope Surface

Curve Loop(7) = {22,19,-8,-18};
Curve Loop(8) = {20,11,-21,-23};
Curve Loop(9) = {18,26,-20,-25};
Curve Loop(10) = {24,21,-27,-19};
Curve Loop(11) = {8,27,-11,-26};

Plane Surface(7) = {7};
Plane Surface(8) = {8};
Plane Surface(9) = {9};
Plane Surface(10) = {10};
Plane Surface(11) = {11};

// Mesh of the Fluid

Curve Loop(12) = {7,26,-10,-13};
Curve Loop(13) = {5,3,-28,-1};
Curve Loop(14) = {1,29,18,-7,-14};
Curve Loop(15) = {15,10,-20,-30,-3};
Curve Loop(16) = {5,15,-13,-14};

Curve Loop(17) = {39,35,-29};
Curve Loop(18) = {30,-38,-40};
Curve Loop(19) = {40,-34,-39,28};

Plane Surface(12) = {12};
Plane Surface(13) = {13};
Plane Surface(14) = {14};
Plane Surface(15) = {15};
Plane Surface(16) = {16};

Plane Surface(17) = {17};
Plane Surface(18) = {18};
Plane Surface(19) = {19};

Surface Loop(2) = {6,9,12,13,14,15,16,17,18,19};
Volume(2) = {2};
Physical Volume("Fluid") = {2};

// Reservoir Surface

Curve Loop(20) = {2,16,-9,-19,-22,-29};
Curve Loop(21) = {12,-17,-4,30,23,21};
Curve Loop(22) = {4,-6,-2,28};

Plane Surface(20) = {20};
Plane Surface(21) = {21};
Plane Surface(22) = {22};

// Physical Surfaces

Physical Surface("FreeSurface") = {12};
Physical Surface("FSInterface") = {2,3,4,5,6};
Physical Surface("Reservoir") = {1,7,8,9,10,11,13,14,15,16,20,21,22};
Physical Surface("Polytope") = {2,3,4,5,6,7,8,9,10,11};
Physical Surface("SolidSide") = {3,4};
Physical Surface("SolidBase") = {1};

Mesh 3;