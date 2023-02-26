Include "../../toolbox_2D.geo";
SetFactory("OpenCASCADE");

N = 10;
M = 101;

// Make the Square

x = 0;
L = 1;
H = 0.1;
y = 0.25;
Call Quad_Square;

// Physical Boundary

Physical Surface("Solid") = {6};
Physical Curve("FSInterface") = {1};
Physical Curve("Clamped") = {2,4};
Physical Curve("Top") = {3};

Mesh.Binary = 1;
Mesh 2;