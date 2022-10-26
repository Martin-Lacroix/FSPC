L = 1;
HS = 0.02;

N = 1;
M = 10;

// Points List

Point(1) = {0,0,0};
Point(2) = {L,0,0};
Point(3) = {L,HS,0};
Point(4) = {0,HS,0};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

// Solid Surface

Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};

Transfinite Line{1} = M;
Transfinite Line{2} = N;
Transfinite Line{3} = M;
Transfinite Line{4} = N;

Transfinite Surface{1};
Recombine Surface{1};

// Boundaries

Physical Surface("Solid") = {1};
Physical Curve("FSInterface") = {3};
Physical Curve("Clamped") = {2,4};
Physical Curve("Bottom") = {1};

Mesh 2;