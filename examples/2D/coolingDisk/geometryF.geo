Include "../../toolbox_2D.geo";

H = 0.25;
R = 0.025;
y = 0.28;
d = H/33;
N = 13;

// Make the Circle

x = 0.2;
Call Hole_Circle;
x = 0.45;
Call Hole_Circle;
x = 0.7;
Call Hole_Circle;

// Make the Circle

L = 0.9;
x = 0.45;
y = 0.125;
Call Tri_Square;

// New Structure Part

p = newp; Point(p) = {0,0.28,0,d};
p = newp; Point(p) = {L,0.28,0,d};
l = newl; Line(l) = {7,8};
l = newl; Line(l) = {6,9};

// Physical Boundary

Physical Curve("Poly_1") = {1};
Physical Curve("Poly_2") = {3};
Physical Curve("Poly_3") = {5};
Physical Curve("FreeSurface") = {9};
Physical Curve("Wall") = {7,8,10,13,14};
Physical Curve("FSInterface") = {1,3,5};
Physical Surface("Fluid") = {12};

Mesh 2;