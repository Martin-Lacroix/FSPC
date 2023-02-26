Include "../../toolbox_2D.geo";
SetFactory("OpenCASCADE");

L = 0.005;
eps = 1e-5;
H = 0.079-eps;
N = 60;
M = 5;

// Make the Solid

x = 0.1+L/2;
y = (0.079+eps)/2;
Call Quad_Square;

// Physical Boundary

Physical Surface("Solid") = {6};
Physical Curve("FSInterface") = {4};
Physical Curve("SolidBase") = {3};

Mesh.Binary = 1;
Mesh 2;