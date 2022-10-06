// Parameters

d = 0.01;

L = 1;
HF = 0.2;
HS = 0.02;

// Points List

Point(1) = {L,HS,0,d};
Point(2) = {0,HS,0,d};
Point(3) = {L,HS+HF,0,d};
Point(4) = {0,HS+HF,0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {1,3};
Line(3) = {3,4};
Line(4) = {4,2};

// Fluid Surface

Curve Loop(2) = {-1,2,3,4};
Plane Surface(2) = {2};
Physical Surface("Fluid") = {2};

// Boundaries

Physical Curve("FSInterface") = {1};
Physical Curve("FreeSurface") = {3};
Physical Curve("Wall") = {2,4};

// Builds 2D Mesh

Mesh 2;
