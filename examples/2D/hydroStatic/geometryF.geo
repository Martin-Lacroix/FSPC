Include "../../toolbox_2D.geo";
SetFactory("OpenCASCADE");

d = 0.01;

// Make the Square

x = 0;
L = 1;
H = 0.2;
y = 0.12;
Call Tri_Square;

// Physical Boundary

Physical Surface("Fluid") = {6};
Physical Curve("FSInterface") = {1};
Physical Curve("FreeSurface") = {3};
Physical Curve("Wall") = {2,4};

Mesh.Binary = 1;
Mesh 2;