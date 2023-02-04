L1 = 0.3;
L2 = 0.5;
L3 = 0.8;

H1 = 0.2;
H2 = 0.1;
H3 = 0.3;

B = 0.13;
S = 0.04;

h = 0.5;
w = 0.02;

d = 0.005;
eps = 1e-3;
N = 100;
M = 5;

// Points List

Point(1) = {L1+L2-eps,S+eps,0,d};
Point(2) = {L1+L2-eps,S+h+eps,0,d};
Point(3) = {L1+L2-w-eps,S+eps,0,d};
Point(4) = {L1+L2-w-eps,S+h+eps,0,d};

Point(5) = {L1,0,0,d};
Point(6) = {L1+L2+L3+S,0,0,d};
Point(7) = {L1+L2+L3+S,H1+H2+H3,0,d};
Point(8) = {L1,H1+H2+H3,0,d};

Point(9) = {L1+L2+S/2,S+B,0,d};
Point(10) = {L1+L2+S/2,H1+H2+H3-S-B,0,d};

Point(11) = {L1,S,0,d};
Point(12) = {L1+L2,S,0,d};
Point(13) = {L1+L2,S+B,0,d};
Point(14) = {L1+L2+S,S+B,0,d};
Point(15) = {L1+L2+S,S,0,d};
Point(16) = {L1+L2+L3+S,S,0,d};

Point(17) = {L1,H1+H2+H3-S,0,d};
Point(18) = {L1+L2,H1+H2+H3-S,0,d};
Point(19) = {L1+L2,H1+H2+H3-S-B,0,d};
Point(20) = {L1+L2+S,H1+H2+H3-S-B,0,d};
Point(21) = {L1+L2+S,H1+H2+H3-S,0,d};
Point(22) = {L1+L2+L3+S,H1+H2+H3-S,0,d};

// Lines List

Line(1) = {3,1};
Line(2) = {1,2};
Line(3) = {2,4};
Line(4) = {4,3};

Line(5) = {5,6};
Line(6) = {6,16};
Line(7) = {16,15};
Line(8) = {15,14};
Circle(9) = {14,9,13};
Line(10) = {13,12};
Line(11) = {12,11};
Line(12) = {11,5};

Line(13) = {8,17};
Line(14) = {17,18};
Line(15) = {18,19};
Circle(16) = {19,10,20};
Line(17) = {20,21};
Line(18) = {21,22};
Line(19) = {22,7};
Line(20) = {7,8};

// Solid Surface

Curve Loop(1) = {1,2,3,4};
Curve Loop(2) = {5,6,7,8,9,10,11,12};
Curve Loop(3) = {13,14,15,16,17,18,19,20};
Plane Surface(1) = {1};

Transfinite Surface{1};
Recombine Surface{1};

Transfinite Line{1} = M;
Transfinite Line{2} = N;
Transfinite Line{3} = M;
Transfinite Line{4} = N;

// Boundaries

Physical Surface("Solid") = {1};
Physical Curve("ToolBot") = {5,6,7,8,9,10,11,12};
Physical Curve("ToolTop") = {13,14,15,16,17,18,19,20};
Physical Curve("FSInterface") = {1,2,3,4};

Mesh.Binary = 1;
Mesh 2;