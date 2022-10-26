B = 0.25;
L1 = 0.15;

b = 0.02;
h = 0.1;
w = 0.005;

N = 40;
M = 10;
P = 4;

// Point List

Point(1) = {L1,(B-b)/2,0};
Point(2) = {L1+w,(B-b)/2,0};
Point(3) = {L1+w,(B+b)/2,0};
Point(4) = {L1,(B+b)/2,0};
Point(5) = {L1,(B-b)/2,h};
Point(6) = {L1+w,(B-b)/2,h};
Point(7) = {L1+w,(B+b)/2,h};
Point(8) = {L1,(B+b)/2,h};

// Line List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};
Line(5) = {5,6};
Line(6) = {6,7};
Line(7) = {7,8};
Line(8) = {8,5};

Line(9) = {1,5};
Line(10) = {2,6};
Line(11) = {3,7};
Line(12) = {4,8};

// Mesh of the Solid

Curve Loop(1) = {-4,-3,-2,-1};
Curve Loop(2) = {5,6,7,8};
Curve Loop(3) = {1,10,-5,-9};
Curve Loop(4) = {3,12,-7,-11};
Curve Loop(5) = {2,11,-6,-10};
Curve Loop(6) = {4,9,-8,-12};

Plane Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};
Plane Surface(5) = {5};
Plane Surface(6) = {6};

Transfinite Surface{1:6};
Recombine Surface{1:6};

Transfinite Line{9} = N;
Transfinite Line{10} = N;
Transfinite Line{11} = N;
Transfinite Line{12} = N;

Transfinite Line{2} = M;
Transfinite Line{4} = M;
Transfinite Line{6} = M;
Transfinite Line{8} = M;

Transfinite Line{1} = P;
Transfinite Line{3} = P;
Transfinite Line{5} = P;
Transfinite Line{7} = P;

Surface Loop(1) = {1,2,3,4,5,6};
Volume(1) = {1};

Transfinite Volume(1);
Recombine Volume(1);

// Physical Surfaces

Physical Surface("FSInterface") = {2,3,4,5,6};
Physical Surface("Clamped") = {1};
Physical Volume("Solid") = {1};

Mesh 3;