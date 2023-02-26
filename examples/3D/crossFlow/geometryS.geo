Include "../../toolbox_3D.geo";
SetFactory("OpenCASCADE");

N = 40;
M = 10;
P = 4;

H = 0.1;
W = 0.02;
L = 0.005;

// Make the Square

y = 0;
z = H/2;
x = 0.15+L/2;
Call Quad_Square;

// Physical Surface

Physical Surface("FSInterface") = {20:24};
Physical Surface("Clamped") = {19};
Physical Volume("Solid") = {26};

Mesh.Binary = 1;
Mesh 3;