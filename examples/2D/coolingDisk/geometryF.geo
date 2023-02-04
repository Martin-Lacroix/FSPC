L = 1;
HF = 0.5;
HS = 0.2;
R = 0.1;

d = 0.02;

// Points List

Point(1) = {L,0,0,d};
Point(2) = {0,0,0,d};
Point(3) = {L,HF,0,d};
Point(4) = {0,HF,0,d};
Point(5) = {0,HF+HS,0,d};
Point(6) = {L,HF+HS,0,d};

Point(7) = {L/2,HF+HS,0,d};
Point(8) = {L/2,HF+HS+R,0,d};
Point(9) = {L/2,HF+HS-R,0,d};

// Lines List

Line(1) = {1,2};
Line(2) = {1,3};
Line(3) = {3,4};
Line(4) = {4,2};
Line(5) = {4,5};
Line(6) = {3,6};

Circle(7) = {8,7,9};
Circle(8) = {9,7,8};

// Fluid Surface

Curve Loop(1) = {-1,2,3,4};
Plane Surface(1) = {1};
Curve Loop(2) = {7,8};

// Boundaries

Physical Surface("Fluid") = {1};
Physical Curve("FSInterface") = {7,8};
Physical Curve("FreeSurface") = {3};
Physical Curve("Wall") = {1,2,4,5,6};

Mesh.Binary = 1;
Mesh 2;