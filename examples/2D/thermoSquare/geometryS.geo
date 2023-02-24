Include "../../toolbox_2D.geo";

x = 0;
y = 0;
N = 51;
M = 51;

// Make the Square

L = 2;
H = 2;
Call Quad_Square;

// Boundaries

Physical Surface("Solid") = {6};
Physical Curve("FSInterface") = {1,2,3,4};

Mesh 2;