d = 0.006;
Nx = 60;
Ny = 5;

L = 1.5;
S = 0.2;
R = 0.05;
H = 0.41;
Ls = 0.35;
A = Asin(0.2);

// Points List

Point(1) = {0,0,0,d};
Point(2) = {L,0,0,d};
Point(3) = {L,H,0,d};
Point(4) = {0,H,0,d};

Point(5) = {S,H/2,0,d};
Point(6) = {S-R,H/2,0,d};

Point(7) = {S+R*Cos(A),H/2+R*Sin(A),0,d};
Point(8) = {S+R*Cos(A),H/2-R*Sin(A),0,d};
Point(9) = {S+R+Ls,H/2+R*Sin(A),0,d};
Point(10) = {S+R+Ls,H/2-R*Sin(A),0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Circle(5) = {6,5,7};
Circle(6) = {6,5,8};

Line(7) = {7,9};
Line(8) = {9,10};
Line(9) = {10,8};
Line(10) = {7,8};

// Solid Mesh

Curve Loop(1) = {6,-10,-5};
Plane Surface(1) = {1};
Recombine Surface{1};

Transfinite Line{7} = Nx;
Transfinite Line{8} = Ny;
Transfinite Line{9} = Nx;
Transfinite Line{10} = Ny;

Curve Loop(2) = {-9,-8,-7,10};
Plane Surface(2) = {2};
Transfinite Surface{2};
Recombine Surface{2};

Physical Surface("Solid") = {1,2};

// Fluid Mesh

Curve Loop(3) = {1,2,3,4};
Plane Surface(3) = {3,-1,-2};
Physical Surface("Fluid") = {3};

// Boundary Domains

Physical Curve("FSInterface") = {6,-9,-8,-7,-5};
Physical Curve("Border") = {1,3};
Physical Curve("Inlet") = {4};
Physical Curve("Outlet") = {2};
Physical Curve("Clamped") = {5,6};

Mesh 2;