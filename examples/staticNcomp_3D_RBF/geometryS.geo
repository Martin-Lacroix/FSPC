// Parameters

d = 0.03;
N = 1;

L = 1;
W = 1;
HS = 0.02;

// Points List

Point(1) = {L,0,0,d};
Point(2) = {0,0,0,d};
Point(3) = {L,0,HS,d};
Point(4) = {0,0,HS,d};

Point(5) = {L,W,0,d};
Point(6) = {0,W,0,d};
Point(7) = {L,W,HS,d};
Point(8) = {0,W,HS,d};

// Lines List

Line(1) = {1,2};
Line(2) = {1,3};
Line(3) = {3,4};
Line(4) = {4,2};

Line(5) = {5,6};
Line(6) = {5,7};
Line(7) = {7,8};
Line(8) = {8,6};

Line(9) = {1,5};
Line(10) = {2,6};
Line(11) = {3,7};
Line(12) = {4,8};

Transfinite Line{2} = N;
Transfinite Line{4} = N;
Transfinite Line{6} = N;
Transfinite Line{8} = N;

// Solid Surface

Curve Loop(1) = {-1,2,3,4};
Curve Loop(2) = {-8,-7,-6,5};
Curve Loop(3) = {6,-11,-2,9};
Curve Loop(4) = {-10,-4,12,8};
Curve Loop(5) = {9,5,-10,-1};
Curve Loop(6) = {-11,3,12,-7};

Plane Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};
Plane Surface(5) = {5};
Plane Surface(6) = {6};

Transfinite Surface{1:6};
Recombine Surface{1:6};

// Solid Volume

Surface Loop(1) = {1,2,3,4,5,6};
Volume(1) = {1};
Physical Volume("Solid") = {1};

Transfinite Volume(1);
Recombine Volume(1);

// Boundaries

Physical Surface("FSInterface") = {6};
Physical Surface("Clamped") = {1,2,3,4};

// Builds 2D Mesh

Mesh 3;