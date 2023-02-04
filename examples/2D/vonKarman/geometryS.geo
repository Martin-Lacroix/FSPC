H = 0.12;
A = 0.055;
L = 0.04;
w = 6e-4;
s = 0.01;

N = 120;
M = 3;

// Points List

Point(1) = {A+s/2,(H-w)/2,0};
Point(2) = {A+s/2+L,(H-w)/2,0};
Point(3) = {A+s/2+L,(H+w)/2,0};
Point(4) = {A+s/2,(H+w)/2,0};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

// Solid Mesh

Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};
Transfinite Surface{1};
Recombine Surface{1};

Transfinite Line{1} = N;
Transfinite Line{2} = M;
Transfinite Line{3} = N;
Transfinite Line{4} = M;

// Physical Boundaries

Physical Surface("Solid") = {1};
Physical Curve("FSInterface") = {1,2,3};
Physical Curve("Clamped") = {4};

Mesh.Binary = 1;
Mesh 2;
