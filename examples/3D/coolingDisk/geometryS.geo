RS = 0.0125;
HS = 0.014;
HF = 0.05;

A = Sqrt(3)/3;
U = (RS/2)*A;
R = RS*A;

N = 15;
M = 12;

// Points List

Point(1) = {0,0,HF+HS};
Point(2) = {U,U,HF+HS+U};
Point(3) = {U,U,HF+HS-U};
Point(4) = {U,-U,HF+HS+U};
Point(5) = {U,-U,HF+HS-U};
Point(6) = {-U,U,HF+HS+U};
Point(7) = {-U,U,HF+HS-U};
Point(8) = {-U,-U,HF+HS+U};
Point(9) = {-U,-U,HF+HS-U};

Point(10) = {R,R,HF+HS+R};
Point(11) = {R,R,HF+HS-R};
Point(12) = {R,-R,HF+HS+R};
Point(13) = {R,-R,HF+HS-R};
Point(14) = {-R,R,HF+HS+R};
Point(15) = {-R,R,HF+HS-R};
Point(16) = {-R,-R,HF+HS+R};
Point(17) = {-R,-R,HF+HS-R};

// Line List

Line(1) = {2,3};
Line(2) = {3,5};
Line(3) = {4,5};
Line(4) = {2,4};
Line(5) = {2,6};
Line(6) = {4,8};
Line(7) = {5,9};
Line(8) = {3,7};
Line(9) = {6,7};
Line(10) = {6,8};
Line(11) = {8,9};
Line(12) = {7,9};

Line(13) = {2,10};
Line(14) = {3,11};
Line(15) = {4,12};
Line(16) = {5,13};
Line(17) = {6,14};
Line(18) = {7,15};
Line(19) = {8,16};
Line(20) = {9,17};

// Circle List

Circle(21) = {10,1,11};
Circle(22) = {11,1,13};
Circle(23) = {12,1,13};
Circle(24) = {10,1,12};
Circle(25) = {10,1,14};
Circle(26) = {12,1,16};
Circle(27) = {13,1,17};
Circle(28) = {11,1,15};
Circle(29) = {14,1,15};
Circle(30) = {14,1,16};
Circle(31) = {16,1,17};
Circle(32) = {15,1,17};

Transfinite Line{1:12} = N;
Transfinite Line{13:20} = M;
Transfinite Line{21:32} = N;

// Curve Loop

Curve Loop(1) = {4,3,-2,-1};
Curve Loop(2) = {12,-11,-10,9};
Curve Loop(3) = {-7,-3,6,11};
Curve Loop(4) = {8,-9,-5,1};
Curve Loop(5) = {7,-12,-8,2};
Curve Loop(6) = {-6,-4,5,10};

Curve Loop(7) = {24,23,-22,-21};
Curve Loop(8) = {-3,15,23,-16};
Curve Loop(9) = {1,14,-21,-13};
Curve Loop(10) = {2,16,-22,-14};
Curve Loop(11) = {-4,13,24,-15};

Curve Loop(12) = {32,-31,-30,29};
Curve Loop(13) = {12,20,-32,-18};
Curve Loop(14) = {10,19,-30,-17};
Curve Loop(15) = {11,20,-31,-19};
Curve Loop(16) = {-9,17,29,-18};

Curve Loop(17) = {-27,-23,26,31};
Curve Loop(18) = {-7,16,27,-20};
Curve Loop(19) = {-6,15,26,-19};
Curve Loop(20) = {3,16,-23,-15};
Curve Loop(21) = {-11,19,31,-20};

Curve Loop(22) = {28,-29,-25,21};
Curve Loop(23) = {8,18,-28,-14};
Curve Loop(24) = {5,17,-25,-13};
Curve Loop(25) = {9,18,-29,-17};
Curve Loop(26) = {-1,13,21,-14};

Curve Loop(27) = {27,-32,-28,22};
Curve Loop(28) = {7,20,-27,-16};
Curve Loop(29) = {8,18,-28,-14};
Curve Loop(30) = {12,20,-32,-18};
Curve Loop(31) = {-2,14,22,-16};

Curve Loop(32) = {-26,-24,25,30};
Curve Loop(33) = {-6,15,26,-19};
Curve Loop(34) = {-5,13,25,-17};
Curve Loop(35) = {4,15,-24,-13};
Curve Loop(36) = {-10,17,30,-19};

// Surface Mesh

For j In {1:36}
    Surface(j) = {j};
EndFor

Transfinite Surface{1:36};
Recombine Surface{1:36};

// Volume Mesh

Surface Loop(1) = {1,2,3,4,5,6};
Surface Loop(2) = {1,7,8,9,10,11};
Surface Loop(3) = {2,12,13,14,15,16};
Surface Loop(4) = {3,17,18,19,20,21};
Surface Loop(5) = {4,22,23,24,25,26};
Surface Loop(6) = {5,27,28,29,30,31};
Surface Loop(7) = {6,32,33,34,35,36};

For j In {1:7}

    Volume(j) = {j};
    Transfinite Volume(j);
    Recombine Volume(j);

EndFor

// Physical Surfaces

Physical Volume("Solid") = {1,2,3,4,5,6,7};
Physical Surface("FSInterface") = {7,12,17,22,27,32};

Mesh.Binary = 1;
Mesh 3;