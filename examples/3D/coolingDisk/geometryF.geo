Include "../../toolbox_3D.geo";
SetFactory("OpenCASCADE");

L = 0.064;
d = 3.7e-3;

// Make the Sphere

x = 0;
y = 0;
z = L;
R = 0.0125;
Call Hole_Sphere;

// Make the Cylinder

x = 0;
y = 0;
z = 0;
R = 0.1;
H = 0.05;
Call Tri_Cylinder;

// New Structure Part

p = newp; Point(p) = {0,0,L,d};
p = newp; Point(p) = {0,-R,L,d};
p = newp; Point(p) = {R,0,L,d};
p = newp; Point(p) = {-R,0,L,d};
p = newp; Point(p) = {0,R,L,d};

// Line List

c = newl; Line(c) = {9,15};
c = newl; Line(c) = {10,16};
c = newl; Line(c) = {11,17};
c = newl; Line(c) = {12,14};
c = newl; Circle(c) = {14,13,15};
c = newl; Circle(c) = {15,13,17};
c = newl; Circle(c) = {17,13,16};
c = newl; Circle(c) = {16,13,14};

// Surface Mesh

k = newcl; Curve Loop(k) = {9,30,34,33};
k = newcl; Curve Loop(k) = {10,32,35,30};
k = newcl; Curve Loop(k) = {11,31,36,32};
k = newcl; Curve Loop(k) = {8,33,37,31};

s = news; BSpline Surface(s) = {38};
s = news; BSpline Surface(s) = {39};
s = news; BSpline Surface(s) = {40};
s = news; BSpline Surface(s) = {41};

// Physical Surface

Physical Volume("Fluid") = {29};
Physical Surface("FSInterface") = {1};
Physical Surface("FreeSurface") = {27};
Physical Surface("Wall") = {22:26,42:45};

Mesh.Binary = 1;
Mesh 3;