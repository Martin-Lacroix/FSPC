// Parameters

d = 0.06;
R = 0.25;

L1 = 0.25+R;
L2 = 0.6-2*R;

L = 0.15+R;
H = -0.125;

D1 = 3.75-10*R;
D2 = 1.25;

HB = 0.75+H+5*R;
RB = 0.375;

// Left Points

Point(1) = {-(L+L1+L2),H-5*R,0,d};
Point(2) = {-(L+L1+L2),H+5*R,0,d};

Point(3) = {-L,H+5*R,0,d};
Point(4) = {-L,H+4*R,0,d};
Point(5) = {-L,H+3*R,0,d};

Point(6) = {-(L+L2),H+3*R,0,d};
Point(7) = {-(L+L2),H+2*R,0,d};
Point(8) = {-(L+L2),H+R,0,d};

Point(9) = {-L,H+R,0,d};
Point(10) = {-L,H,0,d};
Point(11) = {-L,H-R,0,d};

Point(12) = {-(L+L2),H-R,0,d};
Point(13) = {-(L+L2),H-2*R,0,d};
Point(14) = {-(L+L2),H-3*R,0,d};

Point(15) = {-L,H-3*R,0,d};
Point(16) = {-L,H-4*R,0,d};
Point(17) = {-L,H-5*R,0,d};

// Left Lines

Line(1) = {1,17};
Circle(2) = {17,16,15};
Line(3) = {15,14};
Circle(4) = {12,13,14};
Line(5) = {12,11};
Circle(6) = {11,10,9};
Line(7) = {9,8};
Circle(8) = {6,7,8};
Line(9) = {6,5};
Circle(10) = {5,4,3};
Line(11) = {3,2};
Line(12) = {2,1};

// Left Surface

Curve Loop(1) = {1,2,3,-4,5,6,7,-8,9,10,11,12};
Plane Surface(1) = {1};
Physical Surface("SolidL") = {1};
Recombine Surface{1};

// Right Points

Point(18) = {L+L1+L2,-H-5*R,0,d};
Point(19) = {L+L1+L2,-H+5*R,0,d};

Point(20) = {L,-H+5*R,0,d};
Point(21) = {L,-H+4*R,0,d};
Point(22) = {L,-H+3*R,0,d};

Point(23) = {L+L2,-H+3*R,0,d};
Point(24) = {L+L2,-H+2*R,0,d};
Point(25) = {L+L2,-H+R,0,d};

Point(26) = {L,-H+R,0,d};
Point(27) = {L,-H,0,d};
Point(28) = {L,-H-R,0,d};

Point(29) = {L+L2,-H-R,0,d};
Point(30) = {L+L2,-H-2*R,0,d};
Point(31) = {L+L2,-H-3*R,0,d};

Point(32) = {L,-H-3*R,0,d};
Point(33) = {L,-H-4*R,0,d};
Point(34) = {L,-H-5*R,0,d};

// Right Lines

Line(13) = {18,19};
Line(14) = {19,20};
Circle(15) = {20,21,22};
Line(16) = {22,23};
Circle(17) = {25,24,23};
Line(18) = {25,26};
Circle(19) = {26,27,28};
Line(20) = {28,29};
Circle(21) = {31,30,29};
Line(22) = {31,32};
Circle(23) = {32,33,34};
Line(24) = {34,18};

// Right Surface

Curve Loop(2) = {13,14,15,16,-17,18,19,20,-21,22,23,24};
Plane Surface(2) = {2};
Physical Surface("SolidR") = {2};
Recombine Surface{2};

// Ball Points

Point(35) = {-RB,HB,0,d};
Point(36) = {0,HB,0,d};
Point(37) = {RB,HB,0,d};

// Ball Lines

Circle(25) = {35,36,37};
Circle(26) = {37,36,35};

// Ball Surface

Curve Loop(3) = {26,25};
Plane Surface(3) = {3};
Physical Surface("Ball") = {3};
Recombine Surface{3};

// Fluid Points

Point(38) = {-(L+L1+L2),H-(5*R+D1),0,d};
Point(39) = {-(L+L1+L2),H+5*R+D2,0,d};
Point(40) = {L+L1+L2,H+5*R+D2,0,d};
Point(41) = {L+L1+L2,H-(5*R+D1),0,d};

// Fluid Lines

Line(27) = {38,1};
Line(28) = {2,39};
Line(29) = {39,40};
Line(30) = {40,19};
Line(31) = {18,41};
Line(32) = {41,38};

// Fluid Surface

Curve Loop(4) = {27,-12,28,29,30,-13,31,32};
Plane Surface(4) = {4,-1,-2,-3};
Physical Surface("Fluid") = {4};

// Boundaries

Physical Curve("FSInterface") = {1,2,3,4,5,6,7,8,9,10,11,14,15,16,17,18,19,20,21,22,23,24,25,26};
Physical Curve("Slave") = {1,2,3,4,5,6,7,8,9,10,11,14,15,16,17,18,19,20,21,22,23,24};
Physical Curve("Master") = {25,26};

Physical Curve("Reservoir") = {27,28,30,31};
Physical Curve("SolidBase") = {12,13};
Physical Curve("Outlet") = {32};
Physical Curve("Inlet") = {29};

Physical Curve("ExclusionL") = {1,2,3,4,5,6,7,8,9,10,11,12};
Physical Curve("ExclusionR") = {13,14,15,16,17,18,19,20,21,22,23,24};

// Builds 2D Mesh

Mesh 2;