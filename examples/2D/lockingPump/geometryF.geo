U = 0.05;
H = 0.13;
T = 0.025;
S = 0.005;
K = 0.2875;
L = 0.5125;
R = 0.5;

d = 0.01;

// Points List

Point(1) = {K,H,0,d};
Point(2) = {K+T,H,0,d};
Point(3) = {L+K,H,0,d};

Point(4) = {-(L+K),H,0,d};
Point(5) = {-(K+T),H,0,d};
Point(6) = {-K,H,0,d};

Point(7) = {K,-H,0,d};
Point(8) = {K+T,-H,0,d};
Point(9) = {L+K,-H,0,d};

Point(10) = {-(L+K),-H,0,d};
Point(11) = {-(K+T),-H,0,d};
Point(12) = {-K,-H,0,d};

Point(13) = {-(K+H-S),T+S,0,d};
Point(14) = {-(K+H-S+U),T+S,0,d};
Point(15) = {-(K+H-S+U),S,0,d};
Point(16) = {-(K+H-S),S,0,d};
Point(17) = {-(K+H-S+U),T/2+S,0,d};
Point(18) = {-(K+H-S),H,0,0,d};

Point(19) = {K+T-(H-S),T+S,0,d};
Point(20) = {K+T-(H-S+U),T+S,0,d};
Point(21) = {K+T-(H-S+U),S,0,d};
Point(22) = {K+T-(H-S),S,0,d};
Point(23) = {K+T-(H-S+U),T/2+S,0,d};
Point(24) = {K+T-(H-S),H,0,0,d};

Point(25) = {-(K+H-S),-(T+S),0,d};
Point(26) = {-(K+H-S+U),-(T+S),0,d};
Point(27) = {-(K+H-S+U),-S,0,d};
Point(28) = {-(K+H-S),-S,0,d};
Point(29) = {-(K+H-S+U),-(T/2+S),0,d};
Point(30) = {-(K+H-S),-H,0,0,d};

Point(31) = {K+T-(H-S),-(T+S),0,d};
Point(32) = {K+T-(H-S+U),-(T+S),0,d};
Point(33) = {K+T-(H-S+U),-S,0,d};
Point(34) = {K+T-(H-S),-S,0,d};
Point(35) = {K+T-(H-S+U),-(T/2+S),0,d};
Point(36) = {K+T-(H-S),-H,0,0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};

Line(3) = {4,5};
Line(4) = {5,6};
Line(5) = {6,1};

Line(6) = {12,11};
Line(7) = {11,10};

Line(8) = {9,8};
Line(9) = {8,7};
Line(10) = {7,12};

Circle(11) = {5,18,13};
Line(12) = {13,14};
Circle(13) = {14,17,15};
Line(14) = {15,16};
Circle(15) = {16,18,6};

Circle(16) = {1,24,19};
Line(17) = {19,20};
Circle(18) = {20,23,21};
Line(19) = {21,22};
Circle(20) = {22,24,2};

Circle(21) = {12,30,28};
Line(22) = {28,27};
Circle(23) = {27,29,26};
Line(24) = {26,25};
Circle(25) = {25,30,11};

Circle(26) = {8,36,34};
Line(27) = {34,33};
Circle(28) = {33,35,32};
Line(29) = {32,31};
Circle(30) = {31,36,7};

Line(31) = {9,3};
Line(32) = {4,10};

// Fluid Surface

Loop_1 = {32,-7,-25,-24,-23,-22,-21,-10,-30,-29,-28,-27,-26,-8};
Loop_2 = {31,-2,-20,-19,-18,-17,-16,-5,-15,-14,-13,-12,-11,-3};
Curve Loop(3) = {Loop_1[],Loop_2[]};
Plane Surface(3) = {3};

Transfinite Line{1} = 1;
Transfinite Line{4} = 1;
Transfinite Line{6} = 1;
Transfinite Line{9} = 1;

// Make Boundaries

Physical Surface("Fluid") = {3};
Physical Curve("FSInterface") =
{5,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30};
Physical Curve("Border") = {2,3,7,8};
Physical Curve("Outlet") = {31};
Physical Curve("Inlet") = {32};

Physical Curve("Poly1") = {1,16,17,18,19,20};
Physical Curve("Poly2") = {4,11,12,13,14,15};
Physical Curve("Poly3") = {6,21,22,23,24,25};
Physical Curve("Poly4") = {9,26,27,28,29,30};

Mesh.Binary = 1;
Mesh 2;