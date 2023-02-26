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

c = newl; Line(c) = {9,15};
c = newl; Line(c) = {10,16};
c = newl; Line(c) = {11,17};
c = newl; Line(c) = {12,14};
c = newl; Circle(c) = {14,13,15};
c = newl; Circle(c) = {15,13,17};
c = newl; Circle(c) = {17,13,16};
c = newl; Circle(c) = {16,13,14};

k1 = newcl; Curve Loop(k1) = {9,30,34,33};
k2 = newcl; Curve Loop(k2) = {10,32,35,30};
k3 = newcl; Curve Loop(k3) = {11,31,36,32};
k4 = newcl; Curve Loop(k4) = {8,33,37,31};

s = news; BSpline Surface(s) = {k1};
s = news; BSpline Surface(s) = {k2};
s = news; BSpline Surface(s) = {k3};
s = news; BSpline Surface(s) = {k4};

// Physical Surface

Physical Volume("Fluid") = {29};
Physical Surface("FSInterface") = {1};
Physical Surface("FreeSurface") = {27};
Physical Surface("Wall") = {22:26,42:45};

Mesh.Binary = 1;
Mesh 3;