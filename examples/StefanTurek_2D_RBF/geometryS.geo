d = 0.005;

X = 0.2;
Y = 0.2;
R = 0.05;
Ls = 0.35;
A = Asin(0.2);

// Points List

Point(1) = {X+R*Cos(A),Y+R*Sin(A),0,d};
Point(2) = {X+R*Cos(A),Y-R*Sin(A),0,d};
Point(3) = {X+R+Ls,Y+R*Sin(A),0,d};
Point(4) = {X+R+Ls,Y-R*Sin(A),0,d};

// Lines List

Line(1) = {1,3};
Line(2) = {3,4};
Line(3) = {4,2};
Line(4) = {1,2};

// Solid Mesh

Curve Loop(1) = {-3,-2,-1,4};
Plane Surface(1) = {1};
Transfinite Surface{1};
Recombine Surface{1};

Physical Surface("Solid") = {1};

// Boundary Domains

Physical Curve("FSInterface") = {1,2,3};
Physical Curve("Clamped") = {4};

Mesh 2;
