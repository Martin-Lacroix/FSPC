M = 0.05;
H1 = 0.1;
H2 = 0.13;
T = 0.025;
S = 0.005;
K = 0.2875;
L = 0.5125;

R = 0.5;
Y = 0.65;
y = H1+H2;
X = Sqrt(R*R-(y-Y)*(y-Y));

d = 0.01;

// Points List

Point(1) = {K,H2,0,d};
Point(2) = {K+T,H2,0,d};
Point(3) = {L+K,H2,0,d};
Point(4) = {L+K,H1+H2,0,d};
Point(5) = {X,y,0,d};
Point(6) = {-X,y,0,d};
Point(7) = {-(L+K),H1+H2,0,d};
Point(8) = {-(L+K),H2,0,d};
Point(9) = {-(K+T),H2,0,d};
Point(10) = {-K,H2,0,d};
Point(11) = {0,Y,0,d};

Point(12) = {K,-H2,0,d};
Point(13) = {K+T,-H2,0,d};
Point(14) = {L+K,-H2,0,d};
Point(15) = {L+K,-(H1+H2),0,d};
Point(16) = {X,-y,0,d};
Point(17) = {-X,-y,0,d};
Point(18) = {-(L+K),-(H1+H2),0,d};
Point(19) = {-(L+K),-H2,0,d};
Point(20) = {-(K+T),-H2,0,d};
Point(21) = {-K,-H2,0,d};
Point(22) = {0,-Y,0,d};

Point(23) = {-(K+H2-S),T+S,0,d};
Point(24) = {-(K+H2-S+M),T+S,0,d};
Point(25) = {-(K+H2-S+M),S,0,d};
Point(26) = {-(K+H2-S),S,0,d};
Point(27) = {-(K+H2-S+M),T/2+S,0,d};
Point(28) = {-(K+H2-S),H2,0,0,d};

Point(29) = {K+T-(H2-S),T+S,0,d};
Point(30) = {K+T-(H2-S+M),T+S,0,d};
Point(31) = {K+T-(H2-S+M),S,0,d};
Point(32) = {K+T-(H2-S),S,0,d};
Point(33) = {K+T-(H2-S+M),T/2+S,0,d};
Point(34) = {K+T-(H2-S),H2,0,0,d};

Point(35) = {-(K+H2-S),-(T+S),0,d};
Point(36) = {-(K+H2-S+M),-(T+S),0,d};
Point(37) = {-(K+H2-S+M),-S,0,d};
Point(38) = {-(K+H2-S),-S,0,d};
Point(39) = {-(K+H2-S+M),-(T/2+S),0,d};
Point(40) = {-(K+H2-S),-H2,0,0,d};

Point(41) = {K+T-(H2-S),-(T+S),0,d};
Point(42) = {K+T-(H2-S+M),-(T+S),0,d};
Point(43) = {K+T-(H2-S+M),-S,0,d};
Point(44) = {K+T-(H2-S),-S,0,d};
Point(45) = {K+T-(H2-S+M),-(T/2+S),0,d};
Point(46) = {K+T-(H2-S),-H2,0,0,d};

// Lines List

Line(1) = {2,3};
Line(2) = {3,4};
Line(3) = {4,5};
Circle(4) = {5,11,6};
Line(5) = {6,7};
Line(6) = {7,8};
Line(7) = {8,9};
Line(8) = {10,1};

Line(9) = {20,19};
Line(10) = {19,18};
Line(11) = {18,17};
Circle(12) = {17,22,16};
Line(13) = {16,15};
Line(14) = {15,14};
Line(15) = {14,13};
Line(16) = {12,21};

Circle(17) = {9,28,23};
Line(18) = {23,24};
Circle(19) = {24,27,25};
Line(20) = {25,26};
Circle(21) = {26,28,10};

Circle(22) = {1,34,29};
Line(23) = {29,30};
Circle(24) = {30,33,31};
Line(25) = {31,32};
Circle(26) = {32,34,2};

Circle(27) = {21,40,38};
Line(28) = {38,37};
Circle(29) = {37,39,36};
Line(30) = {36,35};
Circle(31) = {35,40,20};

Circle(32) = {13,46,44};
Line(33) = {44,43};
Circle(34) = {43,45,42};
Line(35) = {42,41};
Circle(36) = {41,46,12};

// Solid Surface

Curve Loop(1) = {22,23,24,25,26,1,2,3,4,5,6,7,17,18,19,20,21,8};
Curve Loop(2) = {27,28,29,30,31,9,10,11,12,13,14,15,32,33,34,35,36,16};

Plane Surface(1) = {1};
Plane Surface(2) = {2};

// Make Boundaries

Physical Surface("Top") = {1};
Physical Surface("Bot") = {2};

Physical Curve("FSInterface") =
{8,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36};
Physical Curve("Clamped") = {1,2,3,5,6,7,9,10,11,13,14,15};
Physical Curve("Master") = {17,18,19,20,21,22,23,24,25,26};
Physical Curve("Slave") = {27,28,29,30,31,32,33,34,35,36};

Mesh 2;