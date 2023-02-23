L = 1;
HF = 0.2;
HS = 0.1;

N = 101;
M = 10;

// Points List

Point(1) = {0,HF,0};
Point(2) = {L,HF,0};
Point(3) = {L,HF+HS,0};
Point(4) = {0,HF+HS,0};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

// Solid Surface

Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};

Transfinite Line{1} = N;
Transfinite Line{2} = M;
Transfinite Line{3} = N;
Transfinite Line{4} = M;

Transfinite Surface{1};
Recombine Surface{1};

// Boundaries

Physical Surface("Solid") = {1};
Physical Curve("FSInterface") = {1};
Physical Curve("Clamped") = {2,4};
Physical Curve("Top") = {3};

Mesh.Binary = 1;
Mesh 2;