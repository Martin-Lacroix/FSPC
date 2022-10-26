R = 2.25;
H = 3.75;
s = 0.2;

d = 0.05;
N = 160;
M = 80;
P = 5;

// Points List

Point(1) = {-R,H,0};
Point(2) = {-(R+s),H,0};
Point(3) = {-R,0,0};
Point(4) = {-(R+s),0,0};
Point(5) = {R,H,0};
Point(6) = {R+s,H,0};
Point(7) = {R,0,0};
Point(8) = {R+s,0,0};
Point(9) = {0,0,0};

// Lines List

Line(1) = {1,2};
Line(2) = {2,4};
Line(3) = {4,3};
Line(4) = {3,1};

Line(5) = {7,8};
Line(6) = {8,6};
Line(7) = {6,5};
Line(8) = {5,7};

Circle(9) = {4,9,8};
Circle(10) = {3,9,7};

// Solid Surface

Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};
Transfinite Surface{1};
Recombine Surface{1};

Curve Loop(2) = {5,6,7,8};
Plane Surface(2) = {2};
Transfinite Surface{2};
Recombine Surface{2};

Transfinite Line{9} = N;
Transfinite Line{10} = N;

Transfinite Line{2} = M;
Transfinite Line{4} = M;
Transfinite Line{8} = M;
Transfinite Line{6} = M;

Transfinite Line{1} = P;
Transfinite Line{3} = P;
Transfinite Line{5} = P;
Transfinite Line{7} = P;

Curve Loop(3) = {-3,9,-5,-10};
Plane Surface(3) = {3};
Transfinite Surface{3};
Recombine Surface{3};

// Physical Boundaries

Physical Surface("Solid") = {1,2,3};
Physical Curve("FSInterface") = {4,8,10};
Physical Curve("SolidBase") = {1,7};

Mesh 2;