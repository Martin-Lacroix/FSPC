R = 0.1;
d = 0.02;
N = 20;

// Points List

Point(1) = {0,0,0,d};
Point(2) = {0,R,0,d};
Point(3) = {0,-R,0,d};

// Lines List

Circle(1) = {2,1,3};
Circle(2) = {3,1,2};

// Solid Surface

Curve Loop(1) = {1,2};
Plane Surface(1) = {1};
Transfinite Line{1,2} = N;

// Boundaries

Physical Surface("Solid") = {1};
Physical Curve("FSInterface") = {1,2};

Mesh.Binary = 1;
Mesh 2;