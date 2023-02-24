Include "../../toolbox_2D.geo";

L = 0.2;
H = 3.75;
y = 1.875;

M = 5;
N = 80;
d = 0.05;

// Make the Square

x = -2.35;
Call Quad_Square;

x = 2.35;
Call Quad_Square;

// New Structure Part

p = newp; Point(p) = {0,0,0,d};
c = newc; Circle(c) = {6,9,1};
c = newc; Circle(c) = {5,9,2};

k = newcl; Curve Loop(k) = {14,1,13,7};
s = news; Plane Surface(s) = {k};

Transfinite Line{13,14} = 2*N;
Transfinite Surface{s};

// Physical Boundary

Physical Surface("Solid") = {6,12,16};
Physical Curve("FSInterface") = {2,10,14};
Physical Curve("SolidBase") = {3,9};

Mesh.RecombineAll = 1;
Mesh 2;