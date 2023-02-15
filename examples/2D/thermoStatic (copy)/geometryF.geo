L = 0.4;
R = 0.1;

d = 0.02;
N = 20;

// Points List

Point(1) = {0,0,0,d};
Point(2) = {0,L,0,d};
Point(3) = {0,-L,0,d};
Point(4) = {0,R,0,d};
Point(5) = {0,-R,0,d};

// Lines List

Circle(1) = {2,1,3};
Circle(2) = {3,1,2};
Circle(3) = {4,1,5};
Circle(4) = {5,1,4};

// Fluid Surface

Curve Loop(1) = {1,2};
Curve Loop(2) = {3,4};
Plane Surface(1) = {1,-2};
Transfinite Line{3,4} = N;

// Boundaries

Physical Surface("Fluid") = {1};
Physical Curve("FSInterface") = {3,4};
Physical Curve("Wall") = {1,2};

Mesh.Binary = 1;
Mesh 2;