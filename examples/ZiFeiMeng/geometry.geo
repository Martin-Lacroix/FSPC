H = 0.079;
S = 0.005;
D = 0.14;
L1 = 0.1;
L2 = 0.2;

eps = 1e-5;
d = 1e-3;

// Point List

Point(1) = {0,0,0,d};
Point(2) = {L1,0,0,d};
Point(3) = {L1+S+L2,0,0,d};

Point(4) = {0,D,0,d};
Point(5) = {L1,D,0,d};
Point(6) = {L1+S,D,0,d};
Point(7) = {L1+S+L2,D,0,d};

Point(8) = {L1,H,0,d};
Point(9) = {L1+S,H,0,d};
Point(10) = {L1,eps,0,d};
Point(11) = {L1+S,eps,0,d};

// Line List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {4,1};
Line(4) = {11,9};
Line(5) = {9,8};
Line(6) = {8,10};
Line(7) = {10,11};
Line(8) = {9,6};
Line(9) = {6,5};
Line(10) = {5,8};
Line(11) = {5,4};
Line(12) = {2,10};

// Solid Mesh

Curve Loop(1) = {4,5,6,7};
Plane Surface(1) = {1};
Recombine Surface{1};

Transfinite Surface{1};
Recombine Surface{1};

Physical Surface("Solid") = {1};

// Fluid Mesh

Curve Loop(2) = {1,12,-6,-10,11,3};
Plane Surface(2) = {2};
Physical Surface("Fluid") = {2};

// Boundary Domains

Physical Curve("FreeSurface") = {11};
Physical Curve("FSInterface") = {4,5,6,7};
Physical Curve("Reservoir") = {1,2,3,5,8,9,10};
Physical Curve("Polytope") = {4,8,9,10,6,7};
Physical Curve("SolidBase") = {5};

Mesh 2;