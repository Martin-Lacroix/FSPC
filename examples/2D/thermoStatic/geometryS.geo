R = 2;
d = 0.1;
N = 51;

// Points List

Point(1) = {-R,-R,0,d};
Point(2) = {R,-R,0,d};
Point(3) = {R,R,0,d};
Point(4) = {-R,R,0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

// Solid Surface

Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};
Transfinite Line{1:4} = N;
Transfinite Surface{1};
Recombine Surface{1};

// Boundaries

Physical Surface("Solid") = {1};
Physical Curve("FSInterface") = {1,2,3,4};

Mesh.Binary = 1;
Mesh 2;