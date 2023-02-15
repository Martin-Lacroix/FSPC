L = 0.9;
HF = 0.25;
HS = 0.03;
R = 0.025;
C = 0.2;

d = 0.005;
P = 32;

// Points List

Point(1) = {C,HF+HS,0,d};
Point(2) = {C,HF+HS+R,0,d};
Point(3) = {C,HF+HS-R,0,d};

Point(4) = {L/2,HF+HS,0,d};
Point(5) = {L/2,HF+HS+R,0,d};
Point(6) = {L/2,HF+HS-R,0,d};

Point(7) = {L-C,HF+HS,0,d};
Point(8) = {L-C,HF+HS+R,0,d};
Point(9) = {L-C,HF+HS-R,0,d};

// Lines List

Circle(1) = {2,1,3};
Circle(2) = {3,1,2};

Circle(3) = {5,4,6};
Circle(4) = {6,4,5};

Circle(5) = {8,7,9};
Circle(6) = {9,7,8};

// Fluid Surface

Curve Loop(1) = {1,2};
Plane Surface(1) = {1};
Recombine Surface{1};

Curve Loop(2) = {3,4};
Plane Surface(2) = {2};
Recombine Surface{2};

Curve Loop(3) = {5,6};
Plane Surface(3) = {3};
Recombine Surface{3};

Transfinite Line{1:6} = P;

// Boundaries

Physical Surface("Solid_1") = {1};
Physical Surface("Solid_2") = {2};
Physical Surface("Solid_3") = {3};

Physical Curve("Surf_1") = {1,2};
Physical Curve("Surf_2") = {3,4};
Physical Curve("Surf_3") = {5,6};

Physical Curve("FSInterface") = {1,2,3,4,5,6};
Physical Curve("FreeSurface") = {3};
Physical Curve("Wall") = {1,2,4,5,6};

Mesh.Binary = 1;
Mesh 2;