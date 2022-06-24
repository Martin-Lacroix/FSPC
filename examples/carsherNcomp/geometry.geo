// Parameters

d = 0.005;

L1 = 0.3;
L2 = 0.5;
L3 = 0.8;

H1 = 0.2;
H2 = 0.1;
H3 = 0.3;

F = 0.1;
B = 0.13;
R = 0.02;

S1 = 0.04;
S2 = 0.02;

// Points List

Point(1) = {0,H1,0,d};
Point(2) = {L1-R,H1,0,d};
Point(3) = {L1-R,H1-R,0,d};
Point(4) = {L1,H1-R,0,d};
Point(5) = {L1,0,0,d};
Point(6) = {L1+L2+L3+S1,0,0,d};
Point(7) = {L1+L2+L3+S1,H1+H2+H3,0,d};
Point(8) = {L1,H1+H2+H3,0,d};
Point(9) = {L1,H1+H2+R,0,d};
Point(10) = {L1-R,H1+H2+R,0,d};
Point(11) = {L1-R,H1+H2,0,d};
Point(12) = {0,H1+H2,0,d};

Point(13) = {L1,S1,0,d};
Point(14) = {L1+L2,S1,0,d};
Point(15) = {L1+L2,S1+B,0,d};
Point(16) = {L1+L2+S1,S1+B,0,d};
Point(17) = {L1+L2+S1,S1,0,d};
Point(18) = {L1+L2+L3+S1,S1,0,d};

Point(19) = {L1,H1+H2+H3-S1,0,d};
Point(20) = {L1+L2,H1+H2+H3-S1,0,d};
Point(21) = {L1+L2,H1+H2+H3-S1-B,0,d};
Point(22) = {L1+L2+S1,H1+H2+H3-S1-B,0,d};
Point(23) = {L1+L2+S1,H1+H2+H3-S1,0,d};
Point(24) = {L1+L2+L3+S1,H1+H2+H3-S1,0,d};

Point(25) = {F,H1,0,d};
Point(26) = {F,H1+H2,0,d};
Point(27) = {L1+L2+S1/2,S1+B,0,d};
Point(28) = {L1+L2+S1/2,H1+H2+H3-S1-B,0,d};

// Solid Parameters

PH1 = 0.01;
PL1 = 0.01;
PH2 = 0.04;
PL2 = 0.01;

h = H1+H2+H3-2*S1-PH1-PH2;
Alp = Asin(h/Sqrt(h*h+PL1*PL1));
Bet = Pi/2-Alp;

// Solid Wall Points

Point(29) = {L1+L2-PL1,S1+PH1,0,d};
Point(30) = {L1+L2-PL2,H1+H2+H3-S1-PH2,0,d};
Point(31) = {L1+L2-PL1-S2*Sin(Alp),S1+PH1+S2*Cos(Alp),0,d};
Point(32) = {L1+L2-PL2-S2*Cos(Bet),H1+H2+H3-S1-PH2+S2*Sin(Bet),0,d};

// Lines List

Line(1) = {1,25};
Line(2) = {25,26};
Line(3) = {26,12};
Line(4) = {12,1};

Line(5) = {5,6};
Line(6) = {6,18};
Line(7) = {18,17};
Line(8) = {17,16};
Circle(9) = {16,27,15};
Line(10) = {15,14};
Line(11) = {14,13};
Line(12) = {13,5};

Line(13) = {8,19};
Line(14) = {19,20};
Line(15) = {20,21};
Circle(16) = {21,28,22};
Line(17) = {22,23};
Line(18) = {23,24};
Line(19) = {24,7};
Line(20) = {7,8};

Line(21) = {31,29};
Line(22) = {29,30};
Line(23) = {30,32};
Line(24) = {32,31};

// Border Lines

Line(25) = {25,2};
Circle(26) = {2,3,4};
Line(27) = {4,13};
Line(28) = {26,11};
Circle(29) = {11,10,9};
Line(30) = {9,19};

// Fluid Surface

Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};
Physical Surface("Fluid") = {1};
Transfinite Surface{1};

// Tool Surface

Curve Loop(2) = {5,6,7,8,9,10,11,12};
Plane Surface(2) = {2};
Curve Loop(3) = {13,14,15,16,17,18,19,20};
Plane Surface(3) = {3};
Physical Surface("Tool") = {2,3};

// Solid Surface

Curve Loop(4) = {21,22,23,24};
Plane Surface(4) = {4};
Physical Surface("Solid") = {4};
Transfinite Surface{4};
Recombine Surface{4};

// Boundaries

Physical Curve("Border") = {1,3,25,26,27,28,29,30};
Physical Curve("Master") = {7,8,9,10,11,14,15,16,17,18};
Physical Curve("FSInterface") = {21,22,23,24};
Physical Curve("FreeSurface") = {2};
Physical Curve("Inlet") = {4};

Physical Curve("PolyBot") = {5,6,7,8,9,10,11,12};
Physical Curve("PolyTop") = {13,14,15,16,17,18,19,20};

// Builds 2D Mesh

Mesh 2;