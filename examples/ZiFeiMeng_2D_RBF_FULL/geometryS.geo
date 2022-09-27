H = 0.079;
S = 0.005;
L1 = 0.1;

eps = 1e-5;
d = 1e-3;

// Point List

Point(1) = {L1,H,0,d};
Point(2) = {L1+S,H,0,d};
Point(3) = {L1,eps,0,d};
Point(4) = {L1+S,eps,0,d};

// Line List

Line(1) = {4,2};
Line(2) = {2,1};
Line(3) = {1,3};
Line(4) = {3,4};

// Solid Mesh

Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};
Recombine Surface{1};

Transfinite Surface{1};
Recombine Surface{1};

Physical Surface("Solid") = {1};

// Boundary Domains

Physical Curve("FSInterface") = {1,3,4};
Physical Curve("SolidBase") = {2};

Mesh 2;
