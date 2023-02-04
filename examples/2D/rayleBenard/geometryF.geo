L = 1;
HF = 0.2;
HS = 0.1;

d = 0.01;

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

// Boundaries

Physical Surface("Fluid") = {2};
Physical Curve("FSInterface") = {1};
Physical Curve("Wall") = {2,4};
Physical Curve("Top") = {3};

Mesh.Binary = 1;
Mesh 2;