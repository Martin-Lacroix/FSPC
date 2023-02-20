RS = 0.0125;
HS = 0.014;
HF = 0.05;
RF = 0.1;

d = 3.7e-3;
N = 7;

// Points List

Point(1) = {0,0,0,d};
Point(2) = {RF,0,0,d};
Point(3) = {-RF,0,0,d};
Point(4) = {0,RF,0,d};
Point(5) = {0,-RF,0,d};
Point(6) = {0,0,HF,d};
Point(7) = {RF,0,HF,d};
Point(8) = {-RF,0,HF,d};
Point(9) = {0,RF,HF,d};
Point(10) = {0,-RF,HF,d};
Point(11) = {0,0,HF+HS+RS,d};
Point(12) = {0,-RF,HF+HS+RS,d};
Point(13) = {RF,0,HF+HS+RS,d};
Point(14) = {-RF,0,HF+HS+RS,d};
Point(15) = {0,RF,HF+HS+RS,d};
Point(16) = {0,-RS,HF+HS,d};
Point(17) = {RS,0,HF+HS,d};
Point(18) = {-RS,0,HF+HS,d};
Point(19) = {0,RS,HF+HS,d};
Point(20) = {0,0,HS+HF-RS,d};
Point(21) = {0,0,HF+HS,d};

// Circle List

Circle(1) = {3,1,5};
Circle(2) = {5,1,2};
Circle(3) = {2,1,4};
Circle(4) = {4,1,3};
Circle(5) = {8,6,10};
Circle(6) = {10,6,7};
Circle(7) = {7,6,9};
Circle(8) = {9,6,8};
Circle(9) = {15,11,14};
Circle(10) = {14,11,12};
Circle(11) = {12,11,13};
Circle(12) = {13,11,15};
Circle(13) = {18,21,19};
Circle(14) = {19,21,17};
Circle(15) = {17,21,16};
Circle(16) = {16,21,18};
Circle(17) = {16,21,11};
Circle(18) = {11,21,19};
Circle(19) = {18,21,11};
Circle(20) = {11,21,17};
Circle(21) = {18,21,20};
Circle(22) = {20,21,17};
Circle(23) = {16,21,20};
Circle(24) = {20,21,19};

Transfinite Line{13:24} = N;

// Line List

Line(25) = {9,4};
Line(26) = {7,2};
Line(27) = {3,8};
Line(28) = {10,5};
Line(29) = {7,13};
Line(30) = {9,15};
Line(31) = {8,14};
Line(32) = {12,10};

// Curve Loop

Curve Loop(1) = {26,3,-25,-7};
Curve Loop(2) = {4,27,-8,25};
Curve Loop(3) = {1,-28,-5,-27};
Curve Loop(4) = {2,-26,-6,28};
Curve Loop(5) = {2,3,4,1};
Curve Loop(6) = {5,6,7,8};
Curve Loop(7) = {31,-9,-30,8};
Curve Loop(8) = {10,32,-5,31};
Curve Loop(9) = {6,29,-11,32};
Curve Loop(10) = {7,30,-12,-29};

Curve Loop(11) = {17,-19,-16};
Curve Loop(12) = {-20,-17,-15};
Curve Loop(13) = {-18,20,-14};
Curve Loop(14) = {-13,19,18};
Curve Loop(15) = {23,22,15};
Curve Loop(16) = {24,14,-22};
Curve Loop(17) = {16,21,-23};
Curve Loop(18) = {13,-24,-21};

// Surface Mesh

Surface(1) = {1};
Surface(2) = {2};
Surface(3) = {3};
Surface(4) = {4};
Surface(5) = {5};
Surface(6) = {6};
Surface(7) = {7};
Surface(8) = {8};
Surface(9) = {9};
Surface(10) = {10};
Surface(11) = {11};
Surface(12) = {12};
Surface(13) = {13};
Surface(14) = {14};
Surface(15) = {15};
Surface(16) = {16};
Surface(17) = {17};
Surface(18) = {18};

// Fluid Mesh

Surface Loop(1) = {2,5,4,1,3,6};
Surface Loop(2) = {14,18,17,15,16,13,12,11};
Volume(1) = {1};

// Physical Surfaces

Physical Volume("Fluid") = {1};
Physical Surface("FreeSurface") = {6};
Physical Surface("FSInterface") = {11,12,13,14,15,16,17,18};
Physical Surface("Wall") = {1,2,5,3,4,9,10,7,8};

Mesh.Binary = 1;
Mesh 3;