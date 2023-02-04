L = 0.2;
L1 = 0.1;
L2 = 0.2;

H2 = 0.1;
H1 = 0.05;
R = 0.01;

N = 11;
M = 10;
P = 5;

// Points List

Point(1) = {2*R,R,0};
Point(2) = {-2*R,0,0};
Point(3) = {-R,R,0};
Point(4) = {-R,H1,0};
Point(5) = {0,H1,0};
Point(6) = {R,H1,0};
Point(7) = {R,R,0};
Point(8) = {2*R,0,0};
Point(12) = {-2*R,R,0};

// Lines List

Line(1) = {2,8};
Circle(2) = {2,12,3};
Line(3) = {3,4};
Circle(4) = {6,5,4};
Line(5) = {6,7};
Circle(6) = {7,1,8};

// Solid Mesh

Curve Loop(1) = {1,-6,-5,4,-3,-2};
Plane Surface(1) = {1};

Transfinite Line{1} = M;
Transfinite Line{3} = N;
Transfinite Line{5} = N;
Transfinite Line{2} = P;
Transfinite Line{6} = P;
Transfinite Line{4} = 2*P-1;

// Boundary Domains

Physical Surface("Solid") = {1};
Physical Curve("FSInterface") = {2,3,4,5,6};
Physical Curve("SolidBase") = {1};

Mesh.Binary = 1;
Mesh 2;