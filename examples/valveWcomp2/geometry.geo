// Parameters

f = 6;
d = 0.003;

M = 0.05;
H1 = 0.1;
H2 = 0.13;
T = 0.025;
S = 0.005;
K = 0.2875;
L = 0.5125;

R = 0.5;
k = 0.02;
Y = 0.65;
y = H1+H2;
X = Sqrt(R*R-(y-Y)*(y-Y));

// Top Wall Points

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

// Top Wall Lines

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,5};
Circle(5) = {5,11,6};
Line(6) = {6,7};
Line(7) = {7,8};
Line(8) = {8,9};
Line(9) = {9,10};
Line(10) = {10,1};

// Bot Wall Points

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

// Bot Wall Lines

Line(11) = {21,20};
Line(12) = {20,19};
Line(13) = {19,18};
Line(14) = {18,17};
Circle(15) = {17,22,16};
Line(16) = {16,15};
Line(17) = {15,14};
Line(18) = {14,13};
Line(19) = {13,12};
Line(20) = {12,21};

// Top Valve Points

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

// Top Valve Lines

Circle(21) = {9,28,23};
Line(22) = {23,24};
Circle(23) = {24,27,25};
Line(24) = {25,26};
Circle(25) = {26,28,10};

Circle(26) = {1,34,29};
Line(27) = {29,30};
Circle(28) = {30,33,31};
Line(29) = {31,32};
Circle(30) = {32,34,2};

// Bot Valve Points

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

// Bot Valve Lines

Circle(31) = {21,40,38};
Line(32) = {38,37};
Circle(33) = {37,39,36};
Line(34) = {36,35};
Circle(35) = {35,40,20};

Circle(36) = {13,46,44};
Line(37) = {44,43};
Circle(38) = {43,45,42};
Line(39) = {42,41};
Circle(40) = {41,46,12};

// Fluid Lines

Line(41) = {14,3};
Line(42) = {8,19};

// Top Wall Surface

Curve Loop(1) = {26,27,28,29,30,2,3,4,5,6,7,8,21,22,23,24,25,10};
Plane Surface(1) = {1};
Physical Surface("SolidTop") = {1};

// Bot Wall Surface

Curve Loop(2) = {31,32,33,34,35,12,13,14,15,16,17,18,36,37,38,39,40,20};
Plane Surface(2) = {2};
Physical Surface("SolidBot") = {2};

// Fluid Surface

Curve Loop(3) =
{42,-12,-35,-34,-33,-32,-31,-20,-40,-39,-38,-37,-36,-18,
41,-2,-30,-29,-28,-27,-26,-10,-25,-24,-23,-22,-21,-8};
Plane Surface(3) = {3};
Physical Surface("Fluid") = {3};

// Fluid-Structure Interface

Physical Curve("FSInterface") =
{10,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40};
Physical Curve("Exterior") = {5,15};

// Fixed liquid and solid

Physical Curve("ClampL") = {1,2,8,9,11,12,18,19};
Physical Curve("ClampS") = {1,2,3,4,6,7,8,9,11,12,13,14,16,17,18,19};

// For BC and contact

Physical Curve("Inlet") = {42};
Physical Curve("Outlet") = {41};
Physical Curve("Master") = {21,22,23,24,25,26,27,28,29,30};
Physical Curve("Slave") = {31,32,33,34,35,36,37,38,39,40};

// Exclusion Groups

Physical Curve("Poly1") = {1,26,27,28,29,30};
Physical Curve("Poly2") = {9,21,22,23,24,25};
Physical Curve("Poly3") = {11,31,32,33,34,35};
Physical Curve("Poly4") = {19,36,37,38,39,40};

// Fluid Mesh Size

Physical Curve("LocalHchar") =
{21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40};

Field[1] = Distance;
Field[1].CurvesList =
{21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40};

Field[2] = MathEval;
Field[2].F = Sprintf("%g*F1*%g/(%g/2)+%g",f,d,L,d);

// Makes the Mesh

Field[3] = Min;
Field[3].FieldsList = {2};
Background Field = 3;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Algorithm = 5;
Mesh 2;