L = 1;
HF = 0.2;

d = 0.01;
N = 101;

// Points List

Point(1) = {L,0,0,d};
Point(2) = {0,0,0,d};
Point(3) = {L,HF,0,d};
Point(4) = {0,HF,0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {1,3};
Line(3) = {3,4};
Line(4) = {4,2};

// Fluid Surface

Curve Loop(2) = {-1,2,3,4};
Plane Surface(2) = {2};
Transfinite Line{3} = N;

// Boundaries

Physical Surface("Fluid") = {2};
Physical Curve("FSInterface") = {3};
Physical Curve("Wall") = {1,2,4};

Mesh.Binary = 1;
Mesh 2;