L = 0.146;
w = 0.012;
h = 0.08;

N = 40;
M = 8;

// Points List

Point(1) = {2*L,0,0};
Point(2) = {2*L,h,0};
Point(3) = {2*L+w,h,0};
Point(4) = {2*L+w,0,0};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {1,4};

// Solid Surface

Curve Loop(2) = {-3,-2,-1,4};
Plane Surface(2) = {2};
Transfinite Surface{2};
Recombine Surface{2};

Transfinite Line{1} = N;
Transfinite Line{2} = M;
Transfinite Line{3} = N;
Transfinite Line{4} = M;

// Physical Boundaries

Physical Curve("FSInterface") = {1,2,3};
Physical Curve("SolidBase") = {4};
Physical Surface("Solid") = {2};

Mesh 2;