H = 0.1;
L3 = 0.1;
S = 0.001;

N = 80;
M = 2;

// Points List

Point(1) = {0,-S,0};
Point(2) = {L3,-S,0};
Point(3) = {L3,0,0};
Point(4) = {0,0,0};
Point(5) = {L3,S,0};
Point(6) = {0,S,0};

// Lines List

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {3,5};
Line(5) = {5,6};
Line(6) = {6,4};
Line(7) = {4,1};

// Solid Mesh

Curve Loop(1) = {1,2,3,7};
Plane Surface(1) = {1};
Transfinite Surface{1};
Recombine Surface{1};

Curve Loop(2) = {-3,4,5,6};
Plane Surface(2) = {2};
Transfinite Surface{2};
Recombine Surface{2};

Transfinite Line{1} = N;
Transfinite Line{2} = M;
Transfinite Line{3} = N;
Transfinite Line{4} = M;
Transfinite Line{5} = N;
Transfinite Line{6} = M;
Transfinite Line{7} = M;

// Physical Boundaries

Physical Surface("Iron") = {2};
Physical Surface("Copper") = {1};
Physical Curve("FSInterface") = {1,2,4,5,6,7};
Physical Curve("Clamped") = {6,7};

Mesh.Binary = 1;
Mesh 2;