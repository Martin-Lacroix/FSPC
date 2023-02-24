Include "../../toolbox_2D.geo";

C1 = 0.28;
C2 = 0.82;

D = 0.3;
H = 0.1;
S = 0.25;
A = 0.9;
R = 0.02;

d = 0.005;
eps = 1e-3;
N = 100;
M = 5;

// Make the Fluid

y = 0;
x = 0.05;
L = 0.1;
Call Tri_Square;

// New Structure Part

c = newc; Circle(c) = {C1,H/2+R,0,R,-Pi/2,0};
c = newc; Circle(c) = {C2,S/2+R,0,R,-Pi,0};

p = newp; Point(p) = {C1+R,D,0,d};
p = newp; Point(p) = {C2-R,D,0,d};
p = newp; Point(p) = {C2+R,D,0,d};
p = newp; Point(p) = {C2+R+A,D,0,d};

l = newl; Line(l) = {3,5};
l = newl; Line(l) = {6,9};
l = newl; Line(l) = {9,10};
l = newl; Line(l) = {10,7};
l = newl; Line(l) = {8,11};
l = newl; Line(l) = {11,12};

Rotate{{1,0,0},{0,0,0},Pi}{Duplicata{Line{5:14};}};

// Make the Solid

H = 0.55;
L = 0.02;
y = eps-(D-H/2);
x = C2-R-L/2-eps;
Call Hole_Square;

// Physical Boundary

Physical Surface("Fluid") = {6};
Physical Curve("Border") = {1,3,7:22};
Physical Curve("FSInterface") = {23:26};
Physical Curve("FreeSurface") = {2};
Physical Curve("Inlet") = {4};

Mesh.MeshSizeMax = d;
Mesh 2;