L = 1;
HF = 0.5;
HS = 0.2;
R = 0.1;

d = 0.02;

// Points List

Point(1) = {L/2,HF+HS,0,d};
Point(2) = {L/2,HF+HS+R,0,d};
Point(3) = {L/2,HF+HS-R,0,d};

// Lines List

Circle(1) = {2,1,3};
Circle(2) = {3,1,2};

// Solid Surface

Curve Loop(1) = {1,2};
Plane Surface(1) = {1};
Recombine Surface{1};

// Boundaries

Physical Surface("Solid") = {1};
Physical Curve("FSInterface") = {1,2};

Mesh 2;