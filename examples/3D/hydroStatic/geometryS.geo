Include "../../toolbox_3D.geo";
SetFactory("OpenCASCADE");

L = 1;
W = 1;
H = 0.02;
M = 51;
P = 51;
N = 3;

// Make the Square

x = 0;
y = 0;
z = H/2;
Call Quad_Square;

// Physical Surface

Physical Volume("Solid") = {26};
Physical Surface("FSInterface") = {20};
Physical Surface("Clamped") = {21:24};

Mesh.Binary = 1;
Mesh 3;