Include "../../toolbox_3D.geo";
SetFactory("OpenCASCADE");

L = 1;
W = 1;
H = 0.2;
d = 0.05;

// Make the Square

x = 0;
y = 0;
z = H/2+0.02;
Call Tri_Square;

// Physical Surface

Physical Volume("Fluid") = {1};
Physical Surface("FSInterface") = {5};
Physical Surface("FreeSurface") = {6};
Physical Surface("Wall") = {1:4};

Mesh.Binary = 1;
Mesh 3;