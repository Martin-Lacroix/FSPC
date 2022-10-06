// Parameters

N = 1;
d = 0.1;

L = 1;
HS = 0.02;

// Points List

Point(1) = {0,0,0,d};
Point(2) = {L,0,0,d};
Point(3) = {L,HS,0,d};
Point(4) = {0,HS,0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

// Solid Surface

Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};
Physical Surface("Solid") = {1};

Transfinite Line{2} = N;
Transfinite Line{4} = N;

Transfinite Surface{1};
Recombine Surface{1};

// Boundaries

Physical Curve("FSInterface") = {3};
Physical Curve("Clamped") = {2,4};
Physical Curve("Bottom") = {1};

// Builds 2D Mesh

Mesh 2;
