L = 0.15;
s = 0.015;
h = 0.07;
d = 0.002;

// Points List

Point(1) = {2*L,0,0,d};
Point(2) = {2*L,h,0,d};
Point(3) = {2*L+s,h,0,d};
Point(4) = {2*L+s,0,0,d};

// Lines List

Line(1) = {2,1};
Line(2) = {3,2};
Line(3) = {4,3};
Line(4) = {1,4};

// Solid Surface

Curve Loop(2) = {1,2,3,4};
Plane Surface(2) = {2};
Transfinite Surface{2};
Recombine Surface{2};

// Physical Boundaries

Physical Curve("FSInterface") = {1,2,3,4};
Physical Curve("SolidBase") = {4};
Physical Surface("Solid") = {2};

Mesh 2;
