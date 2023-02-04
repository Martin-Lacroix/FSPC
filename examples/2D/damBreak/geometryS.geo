L = 0.146;
w = 0.012;
h = 0.08;

N = 40;
M = 8;

// Points List

Point(1) = {2*L,0,0};
Point(2) = {2*L+w,0,0};
Point(3) = {2*L+w,h,0};
Point(4) = {2*L,h,0};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

// Solid Surface

Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};
Transfinite Surface{1};
Recombine Surface{1};

Transfinite Line{1} = M;
Transfinite Line{2} = N;
Transfinite Line{3} = M;
Transfinite Line{4} = N;

// Physical Boundaries

Physical Surface("Solid") = {1};
Physical Curve("FSInterface") = {2,3,4};
Physical Curve("SolidBase") = {1};

Mesh.Binary = 1;
Mesh 2;