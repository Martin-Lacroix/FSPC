Ly = 0.3;

S = 0.6;
Sx = 0.03;
Sy = 0.1;
Sz = 0.2;

N = 20;
M = 10;
P = 4;

// Points List

Point(1) = {S,(Ly-Sy)/2,0};
Point(2) = {S+Sx,(Ly-Sy)/2,0};
Point(3) = {S+Sx,(Ly+Sy)/2,0};
Point(4) = {S,(Ly+Sy)/2,0};

Point(5) = {S,(Ly-Sy)/2,Sz};
Point(6) = {S+Sx,(Ly-Sy)/2,Sz};
Point(7) = {S+Sx,(Ly+Sy)/2,Sz};
Point(8) = {S,(Ly+Sy)/2,Sz};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Line(5) = {5,6};
Line(6) = {6,7};
Line(7) = {7,8};
Line(8) = {8,5};

Line(9) = {1,5};
Line(10) = {2,6};
Line(11) = {3,7};
Line(12) = {4,8};

// Surface List

Curve Loop(7) = {-4,-3,-2,-1};
Curve Loop(8) = {5,6,7,8};
Curve Loop(9) = {1,10,-5,-9};
Curve Loop(10) = {12,-7,-11,3};
Curve Loop(11) = {2,11,-6,-10};
Curve Loop(12) = {9,-8,-12,4};

Plane Surface(7) = {7};
Plane Surface(8) = {8};
Plane Surface(9) = {9};
Plane Surface(10) = {10};
Plane Surface(11) = {11};
Plane Surface(12) = {12};

Transfinite Surface{7:12};
Recombine Surface{7:12};

// Mesh of the Solid

Surface Loop(1) = {7,8,9,10,11,12};
Volume(1) = {1};

Transfinite Volume(1);
Recombine Volume(1);

Transfinite Line{9} = N;
Transfinite Line{10} = N;
Transfinite Line{11} = N;
Transfinite Line{12} = N;

Transfinite Line{2} = M;
Transfinite Line{4} = M;
Transfinite Line{6} = M;
Transfinite Line{8} = M;

Transfinite Line{1} = P;
Transfinite Line{3} = P;
Transfinite Line{5} = P;
Transfinite Line{7} = P;

// Physical Surfaces

Physical Volume("Solid") = {1};
Physical Surface("FSInterface") = {8,9,10,11,12};
Physical Surface("Clamped") = {7};

Mesh.Binary = 1;
Mesh 3;