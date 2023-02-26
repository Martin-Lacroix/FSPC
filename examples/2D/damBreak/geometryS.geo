Include "../../toolbox_2D.geo";
SetFactory("OpenCASCADE");

N = 40;
M = 8;

// Make the Solid

y = 0.04;
H = 0.08;
x = 0.298;
L = 0.012;
Call Quad_Square;

// Physical Boundary

Physical Surface("Solid") = {6};
Physical Curve("FSInterface") = {2,3,4};
Physical Curve("SolidBase") = {1};

Mesh.Binary = 1;
Mesh 2;