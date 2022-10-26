L1 = 0.3;
L2 = 0.5;
L3 = 0.8;

H1 = 0.2;
H2 = 0.1;
H3 = 0.3;

F = 0.1;
B = 0.13;
R = 0.02;
S = 0.04;

h = 0.5;
w = 0.02;

d = 0.005;
eps = 1e-3;
N = 100;
M = 5;

// Points List

Point(1) = {0,H1,0,d};
Point(2) = {L1-R,H1,0,d};
Point(3) = {L1-R,H1-R,0,d};
Point(4) = {L1,H1-R,0,d};

Point(5) = {L1,H1+H2+R,0,d};
Point(6) = {L1-R,H1+H2+R,0,d};
Point(7) = {L1-R,H1+H2,0,d};
Point(8) = {0,H1+H2,0,d};

Point(9) = {L1,S,0,d};
Point(10) = {L1+L2,S,0,d};
Point(11) = {L1+L2,S+B,0,d};
Point(12) = {L1+L2+S,S+B,0,d};
Point(13) = {L1+L2+S,S,0,d};
Point(14) = {L1+L2+L3+S,S,0,d};

Point(15) = {L1,H1+H2+H3-S,0,d};
Point(16) = {L1+L2,H1+H2+H3-S,0,d};
Point(17) = {L1+L2,H1+H2+H3-S-B,0,d};
Point(18) = {L1+L2+S,H1+H2+H3-S-B,0,d};
Point(19) = {L1+L2+S,H1+H2+H3-S,0,d};
Point(20) = {L1+L2+L3+S,H1+H2+H3-S,0,d};

Point(21) = {F,H1,0,d};
Point(22) = {F,H1+H2,0,d};
Point(23) = {L1+L2+S/2,S+B,0,d};
Point(24) = {L1+L2+S/2,H1+H2+H3-S-B,0,d};

Point(29) = {L1+L2-eps,S+eps,0,d};
Point(30) = {L1+L2-eps,S+h+eps,0,d};
Point(31) = {L1+L2-w-eps,S+eps,0,d};
Point(32) = {L1+L2-w-eps,S+h+eps,0,d};

// Lines List

Line(1) = {1,21};
Line(2) = {21,22};
Line(3) = {22,8};
Line(4) = {8,1};

Line(5) = {10,13};
Line(6) = {19,16};

Line(7) = {14,13};
Line(8) = {13,12};
Circle(9) = {12,23,11};
Line(10) = {11,10};
Line(11) = {10,9};

Line(12) = {15,16};
Line(13) = {16,17};
Circle(14) = {17,24,18};
Line(15) = {18,19};
Line(16) = {19,20};

Line(17) = {31,29};
Line(18) = {29,30};
Line(19) = {30,32};
Line(20) = {32,31};

Line(21) = {21,2};
Circle(22) = {2,3,4};
Line(23) = {4,9};
Line(24) = {22,7};
Circle(25) = {7,6,5};
Line(26) = {5,15};

// Fluid Surface

Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};
Transfinite Surface{1};

Transfinite Line{29} = M;
Transfinite Line{30} = N;
Transfinite Line{31} = M;
Transfinite Line{32} = N;

// Boundaries

Physical Surface("Fluid") = {1};
Physical Curve("Border") = {1,3,5,6,7,8,9,10,11,12,13,14,15,16,21,22,23,24,25,26};
Physical Curve("FSInterface") = {17,18,19,20};
Physical Curve("PolyTop") = {6,13,14,15};
Physical Curve("PolyBot") = {5,8,9,10};
Physical Curve("FreeSurface") = {2};
Physical Curve("Inlet") = {4};

Mesh 2;