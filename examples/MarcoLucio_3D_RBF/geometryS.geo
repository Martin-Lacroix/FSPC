L = 0.146;
w = 0.012;
h = 0.08;
D = 0.2;

d = 0.005;
eps = 1e-5;

// Points List

Point(1) = {2*L,0,0,d};
Point(2) = {2*L+w,0,0,d};
Point(3) = {2*L,D,0,d};
Point(4) = {2*L+w,D,0,d};
Point(5) = {2*L,eps,h,d};
Point(6) = {2*L+w,eps,h,d};
Point(7) = {2*L,D-eps,h,d};
Point(8) = {2*L+w,D-eps,h,d};

// Lines List

Line(1) = {1,2};
Line(2) = {3,4};
Line(3) = {2,4};
Line(4) = {1,3};
Line(5) = {1,5};
Line(6) = {2,6};
Line(7) = {3,7};
Line(8) = {4,8};
Line(9) = {5,6};
Line(10) = {7,8};
Line(11) = {5,7};
Line(12) = {6,8};

// Mesh of the Solid

Curve Loop(1) = {2,-3,-1,4};
Curve Loop(2) = {9,12,-10,-11};
Curve Loop(3) = {3,8,-12,-6};
Curve Loop(4) = {5,11,-7,-4};
Curve Loop(5) = {1,6,-9,-5};
Curve Loop(6) = {7,10,-8,-2};

Plane Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};
Plane Surface(5) = {5};
Plane Surface(6) = {6};

Transfinite Surface{1:6};
Recombine Surface{1:6};

Surface Loop(1) = {1,2,3,4,5,6};
Volume(1) = {1};
Physical Volume("Solid") = {1};

Transfinite Volume(1);
Recombine Volume(1);

// Physical Surfaces

Physical Surface("FSInterface") = {1,2,3,4,5,6};
Physical Surface("SolidSide") = {5,6};
Physical Surface("SolidBase") = {1};

Mesh 3;