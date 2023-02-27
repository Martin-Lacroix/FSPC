Include "../../toolbox_3D.geo";
SetFactory("OpenCASCADE");

N = 20;
M = 10;
P = 4;

// Make the Solid

L = 0.03;
H = 0.3;
W = 0.1;

y = 0;
z = H/2;
x = L/2+0.6;
Call Quad_Square;

// Physical Surface

Physical Volume("Solid") = {26};
Physical Surface("FSInterface") = {20:24};
Physical Surface("Clamped") = {19};

Mesh.Binary = 1;
Mesh 3;