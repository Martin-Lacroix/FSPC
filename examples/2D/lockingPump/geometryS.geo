U = 0.05;
H1 = 0.1;
H2 = 0.13;
T = 0.025;
S = 0.005;
K = 0.2875;

R = 0.5;
Y = 0.65;
y = H1+H2;
X = Sqrt(R*R-(y-Y)*(y-Y));

d = 5e-3;

// Points List

Point(1) = {K,H2,0,d};
Point(2) = {K+T,H2,0,d};
Point(3) = {K+T,H1+H2,0,d};
Point(4) = {X,y,0,d};
Point(5) = {-X,y,0,d};
Point(6) = {-(K+T),H1+H2,0,d};
Point(7) = {-(K+T),H2,0,d};
Point(8) = {-K,H2,0,d};
Point(9) = {0,Y,0,d};

Point(10) = {K,-H2,0,d};
Point(11) = {K+T,-H2,0,d};
Point(12) = {K+T,-(H1+H2),0,d};
Point(13) = {X,-y,0,d};
Point(14) = {-X,-y,0,d};
Point(15) = {-(K+T),-(H1+H2),0,d};
Point(16) = {-(K+T),-H2,0,d};
Point(17) = {-K,-H2,0,d};
Point(18) = {0,-Y,0,d};

Point(19) = {-(K+H2-S),T+S,0,d};
Point(20) = {-(K+H2-S+U),T+S,0,d};
Point(21) = {-(K+H2-S+U),S,0,d};
Point(22) = {-(K+H2-S),S,0,d};
Point(23) = {-(K+H2-S+U),T/2+S,0,d};
Point(24) = {-(K+H2-S),H2,0,0,d};

Point(25) = {K+T-(H2-S),T+S,0,d};
Point(26) = {K+T-(H2-S+U),T+S,0,d};
Point(27) = {K+T-(H2-S+U),S,0,d};
Point(28) = {K+T-(H2-S),S,0,d};
Point(29) = {K+T-(H2-S+U),T/2+S,0,d};
Point(30) = {K+T-(H2-S),H2,0,0,d};

Point(31) = {-(K+H2-S),-(T+S),0,d};
Point(32) = {-(K+H2-S+U),-(T+S),0,d};
Point(33) = {-(K+H2-S+U),-S,0,d};
Point(34) = {-(K+H2-S),-S,0,d};
Point(35) = {-(K+H2-S+U),-(T/2+S),0,d};
Point(36) = {-(K+H2-S),-H2,0,0,d};

Point(37) = {K+T-(H2-S),-(T+S),0,d};
Point(38) = {K+T-(H2-S+U),-(T+S),0,d};
Point(39) = {K+T-(H2-S+U),-S,0,d};
Point(40) = {K+T-(H2-S),-S,0,d};
Point(41) = {K+T-(H2-S+U),-(T/2+S),0,d};
Point(42) = {K+T-(H2-S),-H2,0,0,d};

// Lines List

Line(1) = {2,3};
Line(2) = {3,4};
Circle(3) = {4,9,5};
Line(4) = {5,6};
Line(5) = {6,7};
Line(6) = {8,1};

Line(7) = {16,15};
Line(8) = {15,14};
Circle(9) = {14,18,13};
Line(10) = {13,12};
Line(11) = {12,11};
Line(12) = {10,17};

Circle(13) = {7,24,19};
Line(14) = {19,20};
Circle(15) = {20,23,21};
Line(16) = {21,22};
Circle(17) = {22,24,8};

Circle(18) = {1,30,25};
Line(19) = {25,26};
Circle(20) = {26,29,27};
Line(21) = {27,28};
Circle(22) = {28,30,2};

Circle(23) = {17,36,34};
Line(24) = {34,33};
Circle(25) = {33,35,32};
Line(26) = {32,31};
Circle(27) = {31,36,16};

Circle(28) = {11,42,40};
Line(29) = {40,39};
Circle(30) = {39,41,38};
Line(31) = {38,37};
Circle(32) = {37,42,10};

// Solid Surface

Curve Loop(1) = {1,2,3,4,5,13,14,15,16,17,6,18,19,20,21,22};
Curve Loop(2) = {7,8,9,10,11,28,29,30,31,32,12,23,24,25,26,27};

Plane Surface(1) = {1};
Plane Surface(2) = {2};

// Make Boundaries

Physical Surface("Top") = {1};
Physical Surface("Bot") = {2};

Physical Curve("FSInterface") =
{13,14,15,16,17,6,18,19,20,21,22,28,29,30,31,32,12,23,24,25,26,27};
Physical Curve("Master") = {13,14,15,16,17,18,19,20,21,22};
Physical Curve("Slave") = {23,24,25,26,27,28,29,30,31,32};
Physical Curve("Clamped") = {1,2,4,5,7,8,10,11};

Mesh.Binary = 1;
Mesh 2;